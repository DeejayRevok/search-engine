from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.update_newspaper.update_newspaper_command_handler.UpdateNewspaperCommandHandler",
            "application.update_newspaper.update_newspaper_command_handler.UpdateNewspaperCommandHandler",
            [
                Argument.no_kw_argument(
                    "@infrastructure.database.repositories"
                    ".sqlalchemy_newspaper_repository.SQLAlchemyNewspaperRepository"
                ),
                Argument.no_kw_argument(
                    "@infrastructure.database.repositories"
                    ".sqlalchemy_named_entity_repository.SQLAlchemyNamedEntityRepository"
                ),
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
