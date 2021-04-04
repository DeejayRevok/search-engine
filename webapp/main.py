"""
Application main module
"""
import sys

from aiohttp.web_app import Application
from aiohttp_apispec import validation_middleware
from news_service_lib import HealthCheck, server_runner, uaa_auth_middleware, get_uaa_service, initialize_apm
from news_service_lib.graphql import setup_graphql_routes
from news_service_lib.storage.sql import create_sql_engine, SqlEngineType, init_sql_db, sql_health_check, \
    SqlSessionProvider

from config import config, CONFIGS_PATH
from log_config import LOG_CONFIG, get_logger
from models import BASE
from services.crud.named_entity_service import NamedEntityService
from services.crud.named_entity_type_service import NamedEntityTypeService
from services.crud.new_service import NewService
from services.crud.newspaper_service import NewspaperService
from services.crud.noun_chunk_service import NounChunkService
from services.crud.source_service import SourceService
from services.crud.user_service import UserService
from services.index_service import IndexService
from services.news_manager_service import NewsManagerService
from webapp.definitions import API_VERSION, health_check, ALEMBIC_INI_PATH
from webapp.event_bus import setup_event_bus
from webapp.graph import schema
from webapp.graph.utils.middlewares import SQLMiddleware
from webapp.middlewares import error_middleware
from webapp.views import index_views


async def shutdown(app: Application):
    """
    Application shutdown handle

    Args:
        app: application to shutdown
    """
    await app['index_service'].shutdown()


def init_search_engine(app: Application) -> Application:
    """
    Initialize the web application

    Args:
        app: configuration profile to use

    Returns: web application initialized
    """
    storage_engine = create_sql_engine(SqlEngineType.MYSQL, **config.storage)
    app['storage_engine'] = storage_engine

    init_sql_db(BASE, storage_engine, alembic_ini_path=ALEMBIC_INI_PATH)

    if not sql_health_check(storage_engine):
        sys.exit(1)

    sql_session_provider = SqlSessionProvider(storage_engine)
    app['session_provider'] = sql_session_provider
    BASE.query = sql_session_provider.query_property

    app['source_service'] = SourceService(sql_session_provider)
    app['new_service'] = NewService(sql_session_provider)
    app['named_entity_service'] = NamedEntityService(sql_session_provider)
    app['named_entity_type_service'] = NamedEntityTypeService(sql_session_provider)
    app['noun_chunks_service'] = NounChunkService(sql_session_provider)
    app['newspaper_service'] = NewspaperService(sql_session_provider)
    app['user_service'] = UserService(sql_session_provider)

    initialize_apm(app, config)
    setup_event_bus()

    app['index_service'] = IndexService(app)

    app['news_manager_service'] = NewsManagerService(**config.news_manager)

    app['uaa_service'] = get_uaa_service(config.uaa)

    HealthCheck(app, health_check)

    setup_graphql_routes(app, schema, get_logger(), middlewares=[SQLMiddleware(app['session_provider'])])
    index_views.setup_routes(app)

    app.middlewares.append(error_middleware)
    app.middlewares.append(uaa_auth_middleware)
    app.middlewares.append(validation_middleware)

    app.on_shutdown.append(shutdown)

    return app


if __name__ == '__main__':
    server_runner('Search Engine', init_search_engine, API_VERSION, CONFIGS_PATH, config, LOG_CONFIG, get_logger)
