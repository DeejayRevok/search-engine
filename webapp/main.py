import sys

from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiohttp_apispec import validation_middleware
from alembic import command
from alembic.config import Config
from elasticapm.contrib.aiohttp import ElasticAPM
from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from news_service_lib.api.utils import setup_cors
from news_service_lib.config_utils import load_config
from news_service_lib.graph.graphql_utils import setup_graphql_routes
from news_service_lib.healthcheck import setup_healthcheck
from news_service_lib.log_utils import add_logstash_handler
from news_service_lib.redis_utils import RedisHealthChecker
from news_service_lib.server_utils import server_args_parser
from news_service_lib.storage.sql.health_checker import SQLHealthChecker

from config import config
from infrastructure.repositories.user_repository import UserRepository
from log_config import LOG_CONFIG, get_logger
from models.base import BASE
from webapp.container_config import container, load
from webapp.definitions import ALEMBIC_INI_PATH
from webapp.event_bus import run_event_bus
from webapp.graph import schema
from webapp.graph.utils.middlewares import SQLMiddleware
from webapp.middlewares import error_middleware, uaa_auth_middleware
from webapp.views.index_view import IndexView


async def shutdown(_):
    await container.get("index_service").shutdown()


def init_sql_db(storage_engine: Engine) -> None:
    BASE.metadata.bind = storage_engine
    if ALEMBIC_INI_PATH:
        alembic_cfg = Config(ALEMBIC_INI_PATH)
        alembic_cfg.set_section_option("alembic", "sqlalchemy.url", str(storage_engine.url))
        if len(inspect(storage_engine).get_table_names()):
            command.upgrade(alembic_cfg, "head")
        else:
            BASE.metadata.create_all()
            command.stamp(alembic_cfg, "head")
    else:
        BASE.metadata.create_all()


def init_search_engine() -> Application:
    app = Application()
    args = server_args_parser("Search Engine")
    loaded_config = load_config(args["configuration"], config, "SEARCH_ENGINE")
    add_logstash_handler(LOG_CONFIG, config.logstash.host, config.logstash.port)
    load()

    app["host"] = loaded_config.server.host
    app["port"] = loaded_config.server.port

    ElasticAPM(app, container.get("apm"))

    logger = get_logger()
    storage_engine = container.get("storage_engine")
    session_provider = container.get("session_provider")
    sql_health_checker = SQLHealthChecker(session_provider, logger)
    if not sql_health_checker.health_check():
        sys.exit(1)

    init_sql_db(storage_engine)
    BASE.query = session_provider.query_property

    setup_healthcheck(app, sql_health_checker)

    container.get("index_service")
    redis_config = config.redis
    redis_healthchecker = RedisHealthChecker(**redis_config)
    run_event_bus(config.redis, redis_healthchecker, logger, UserRepository(session_provider, logger))

    setup_graphql_routes(app, schema, logger, middlewares=[SQLMiddleware(session_provider)])
    IndexView(app, container.get("index_service"), logger)

    setup_cors(app)

    app.middlewares.append(error_middleware)
    app.middlewares.append(uaa_auth_middleware)
    app.middlewares.append(validation_middleware)

    app.on_shutdown.append(shutdown)

    return app


if __name__ == "__main__":
    app = init_search_engine()
    run_app(app, host=app["host"], port=app["port"], access_log=get_logger())
