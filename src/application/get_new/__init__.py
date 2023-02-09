from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.get_new.get_new_query_handler.GetNewQueryHandler",
            "application.get_new.get_new_query_handler.GetNewQueryHandler",
            [
                Argument.no_kw_argument(
                    "@infrastructure.database.repositories.sqlalchemy_new_repository.SQLAlchemyNewRepository"
                ),
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
