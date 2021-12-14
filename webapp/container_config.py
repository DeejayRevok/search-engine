from pypendency.argument import Argument
from pypendency.definition import Definition

from news_service_lib.configurable_container import ConfigurableContainer
from news_service_lib.storage.sql.engine_type import SqlEngineType

from config import config

container: ConfigurableContainer = ConfigurableContainer([], config)


def load():
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
            "news_service_lib.storage.sql.create_sql_engine",
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
            "news_service_lib.storage.sql.SqlSessionProvider",
            [Argument.no_kw_argument("@storage_engine")],
        )
    )

    crud_service_args = [Argument.no_kw_argument("@session_provider")]
    container.set_definition(
        Definition("named_entity_service", "services.crud.named_entity_service.NamedEntityService", crud_service_args)
    )
    container.set_definition(
        Definition(
            "named_entity_type_service",
            "services.crud.named_entity_type_service.NamedEntityTypeService",
            crud_service_args,
        )
    )
    container.set_definition(Definition("new_service", "services.crud.new_service.NewService", crud_service_args))
    container.set_definition(
        Definition("newspaper_service", "services.crud.newspaper_service.NewspaperService", crud_service_args)
    )
    container.set_definition(
        Definition("noun_chunk_service", "services.crud.noun_chunk_service.NounChunkService", crud_service_args)
    )
    container.set_definition(
        Definition("source_service", "services.crud.source_service.SourceService", crud_service_args)
    )
    container.set_definition(Definition("user_service", "services.crud.user_service.UserService", crud_service_args))
    container.set_definition(Definition("index_service", "services.index_service.IndexService"))
    container.set_definition(
        Definition(
            "news_manager_service",
            "services.news_manager_service.NewsManagerService",
            [
                Argument("protocol", "#news_manager.protocol"),
                Argument("host", "#news_manager.host"),
                Argument("port", "#news_manager.port"),
            ],
        )
    )
    container.set_definition(
        Definition("uaa_service", "news_service_lib.uaa_service.get_uaa_service", [Argument.no_kw_argument("#uaa")])
    )
