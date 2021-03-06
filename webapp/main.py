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

from log_config import LOG_CONFIG, get_logger
from models import BASE
from services.crud.named_entity_service import NamedEntityService
from services.crud.named_entity_type_service import NamedEntityTypeService
from services.crud.new_service import NewService
from services.crud.newspaper_service import NewspaperService
from services.crud.noun_chunk_service import NounChunkService
from services.crud.source_service import SourceService
from services.crud.user_new_service import UserNewService
from services.crud.user_source_service import UserSourceService
from services.index_service import IndexService
from services.news_manager_service import NewsManagerService
from webapp.definitions import API_VERSION, CONFIG_PATH, health_check, ALEMBIC_INI_PATH
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
    storage_config = app['config'].get_section('storage')

    storage_engine = create_sql_engine(SqlEngineType.MYSQL, **storage_config)
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
    app['user_source_service'] = UserSourceService(sql_session_provider)
    app['user_new_service'] = UserNewService(sql_session_provider)

    initialize_apm(app)

    app['index_service'] = IndexService(app)

    news_manager_config = app['config'].get_section('NEWS_MANAGER')
    app['news_manager_service'] = NewsManagerService(**news_manager_config)

    uaa_config = app['config'].get_section('UAA')
    app['uaa_service'] = get_uaa_service(uaa_config)

    HealthCheck(app, health_check)

    setup_graphql_routes(app, schema, get_logger(), middlewares=[SQLMiddleware(app['session_provider'])])
    index_views.setup_routes(app)

    app.middlewares.append(error_middleware)
    app.middlewares.append(uaa_auth_middleware)
    app.middlewares.append(validation_middleware)

    app.on_shutdown.append(shutdown)

    return app


if __name__ == '__main__':
    server_runner('Search Engine', init_search_engine, API_VERSION, CONFIG_PATH, LOG_CONFIG, get_logger)
