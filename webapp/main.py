"""
Application main module
"""
import sys

from aiohttp.web_app import Application
from aiohttp_apispec import validation_middleware
from elasticapm.contrib.aiohttp import ElasticAPM

from config import config, CONFIGS_PATH
from log_config import LOG_CONFIG, get_logger
from models import BASE
from news_service_lib import HealthCheck, server_runner
from news_service_lib.graphql import setup_graphql_routes
from news_service_lib.storage.sql import init_sql_db, sql_health_check
from webapp.container_config import container, load
from webapp.definitions import API_VERSION, health_check, ALEMBIC_INI_PATH
from webapp.event_bus import setup_event_bus
from webapp.graph import schema
from webapp.graph.utils.middlewares import SQLMiddleware
from webapp.middlewares import error_middleware, uaa_auth_middleware
from webapp.views import index_views


async def shutdown(_):
    """
    Application shutdown handle
    """
    await container.get('index_service').shutdown()


def init_search_engine(app: Application) -> Application:
    """
    Initialize the web application

    Args:
        app: configuration profile to use

    Returns: web application initialized
    """
    load()
    ElasticAPM(app, container.get('apm'))

    storage_engine = container.get('storage_engine')
    if not sql_health_check(storage_engine):
        sys.exit(1)

    init_sql_db(BASE, storage_engine, alembic_ini_path=ALEMBIC_INI_PATH)

    session_provider = container.get('session_provider')
    BASE.query = session_provider.query_property

    HealthCheck(app, health_check)

    container.get('index_service')
    setup_event_bus()

    setup_graphql_routes(app, schema, get_logger(), middlewares=[SQLMiddleware(session_provider)])
    index_views.setup_routes(app)

    app.middlewares.append(error_middleware)
    app.middlewares.append(uaa_auth_middleware)
    app.middlewares.append(validation_middleware)

    app.on_shutdown.append(shutdown)

    return app


if __name__ == '__main__':
    server_runner('Search Engine', init_search_engine, API_VERSION, CONFIGS_PATH, config, 'SEARCH_ENGINE', LOG_CONFIG,
                  get_logger)
