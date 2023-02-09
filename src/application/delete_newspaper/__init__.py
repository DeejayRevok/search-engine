from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.delete_newspaper.delete_newspaper_command_handler.DeleteNewspaperCommandHandler",
            "application.delete_newspaper.delete_newspaper_command_handler.DeleteNewspaperCommandHandler",
            [
                Argument.no_kw_argument(
                    "@infrastructure.database.repositories"
                    ".sqlalchemy_newspaper_repository.SQLAlchemyNewspaperRepository"
                ),
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
