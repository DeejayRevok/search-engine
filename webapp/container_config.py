from pypendency.argument import Argument
from pypendency.definition import Definition

from log_config import get_logger
from news_service_lib.configurable_container import ConfigurableContainer
from news_service_lib.storage.sql.engine_type import SqlEngineType

from config import config

container: ConfigurableContainer = ConfigurableContainer([], config)


def load():
    logger = get_logger()
    container.set("logger", logger)
    container.set_definition(
        Definition(
            "apm",
            "elasticapm.Client",
            [
                Argument("transactions_ignore_patterns", ["^OPTIONS "]),
                Argument("service_name", "#elastic_apm.service_name"),
                Argument("secret_token", "#elastic_apm.secret_token"),
                Argument("server_url", "#elastic_apm.url"),
            ],
        )
    )
    container.set_definition(
        Definition(
            "storage_engine",
            "news_service_lib.storage.sql.utils.create_sql_engine",
            [
                Argument.no_kw_argument(SqlEngineType.MYSQL),
                Argument("host", "#storage.host"),
                Argument("port", "#storage.port"),
                Argument("user", "#storage.user"),
                Argument("password", "#storage.password"),
                Argument("database", "#storage.database"),
            ],
        )
    )

    container.set_definition(
        Definition(
            "session_provider",
            "news_service_lib.storage.sql.session_provider.SqlSessionProvider",
            [Argument.no_kw_argument("@storage_engine")],
        )
    )

    crud_repository_args = [Argument.no_kw_argument("@session_provider"), Argument.no_kw_argument("@logger")]
    container.set_definition(
        Definition(
            "named_entity_repository",
            "infrastructure.repositories.named_entity_repository.NamedEntityRepository",
            crud_repository_args,
        )
    )
    container.set_definition(
        Definition(
            "named_entity_type_repository",
            "infrastructure.repositories.named_entity_type_repository.NamedEntityTypeRepository",
            crud_repository_args,
        )
    )
    container.set_definition(
        Definition("new_repository", "infrastructure.repositories.new_repository.NewRepository", crud_repository_args)
    )
    container.set_definition(
        Definition(
            "newspaper_repository",
            "infrastructure.repositories.newspaper_repository.NewspaperRepository",
            crud_repository_args,
        )
    )
    container.set_definition(
        Definition(
            "noun_chunk_repository",
            "infrastructure.repositories.noun_chunk_repository.NounChunkRepository",
            crud_repository_args,
        )
    )
    container.set_definition(
        Definition(
            "source_repository", "infrastructure.repositories.source_repository.SourceRepository", crud_repository_args
        )
    )
    container.set_definition(
        Definition(
            "user_repository", "infrastructure.repositories.user_repository.UserRepository", crud_repository_args
        )
    )
    container.set_definition(
        Definition(
            "index_service",
            "services.index_service.IndexService",
            [Argument.no_kw_argument("@logger"), Argument.no_kw_argument("@storage_engine")],
        )
    )
    container.set_definition(
        Definition(
            "news_manager_service",
            "services.news_manager_service.NewsManagerService",
            [
                Argument("protocol", "#news_manager.protocol"),
                Argument("host", "#news_manager.host"),
                Argument("port", "#news_manager.port"),
                Argument("jwt_secret", "#server.jwt_secret"),
                Argument("logger", "@logger"),
            ],
        )
    )
    container.set_definition(
        Definition(
            "uaa_service",
            "news_service_lib.uaa_service.UaaService",
            [
                Argument.no_kw_argument("#uaa.protocol"),
                Argument.no_kw_argument("#uaa.host"),
                Argument.no_kw_argument("#uaa.port"),
            ],
        )
    )
