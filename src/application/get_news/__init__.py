from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.get_news.get_news_query_handler.GetNewsQueryHandler",
            "application.get_news.get_news_query_handler.GetNewsQueryHandler",
            [
                Argument.no_kw_argument(
                    "@infrastructure.database.repositories.sqlalchemy_new_repository.SQLAlchemyNewRepository"
                ),
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
