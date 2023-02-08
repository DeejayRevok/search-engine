from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.get_newspapers.get_newspapers_query_handler.GetNewspapersQueryHandler",
            "application.get_newspapers.get_newspapers_query_handler.GetNewspapersQueryHandler",
            [
                Argument.no_kw_argument(
                    "@infrastructure.database.repositories.sqlalchemy_newspaper_repository.SQLAlchemyNewspaperRepository"
                ),
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
