from bus_station.query_terminal.query_handler_registry import QueryHandlerRegistry
from yandil.container import default_container

from application.get_named_entities.get_named_entities_query_handler import GetNamedEntitiesQueryHandler
from application.get_new.get_new_query_handler import GetNewQueryHandler
from application.get_news.get_news_query_handler import GetNewsQueryHandler
from application.get_newspapers.get_newspapers_query_handler import GetNewspapersQueryHandler


def register() -> None:
    registry = default_container[QueryHandlerRegistry]
    query_handlers = [
        GetNamedEntitiesQueryHandler,
        GetNewQueryHandler,
        GetNewsQueryHandler,
        GetNewspapersQueryHandler,
    ]

    for query_handler in query_handlers:
        registry.register(default_container[query_handler])
