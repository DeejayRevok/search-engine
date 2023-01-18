from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.get_named_entities.get_named_entities_query_handler.GetNamedEntitiesQueryHandler",
            "application.get_named_entities.get_named_entities_query_handler.GetNamedEntitiesQueryHandler",
            [
                Argument.no_kw_argument("@infrastructure.database.repositories.sqlalchemy_named_entity_repository.SQLAlchemyNamedEntityRepository"),
                Argument.no_kw_argument("@logging.Logger")
            ]
        )
    )
