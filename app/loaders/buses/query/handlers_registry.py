from bus_station.query_terminal.query_handler_registry import QueryHandlerRegistry
from yandil.container import default_container


def register() -> None:
    registry = default_container[QueryHandlerRegistry]
    query_handler_fqns = [
        "application.get_named_entities.get_named_entities_query_handler.GetNamedEntitiesQueryHandler",
        "application.get_new.get_new_query_handler.GetNewQueryHandler",
        "application.get_news.get_news_query_handler.GetNewsQueryHandler",
        "application.get_newspapers.get_newspapers_query_handler.GetNewspapersQueryHandler",
    ]

    for query_handler_fqn in query_handler_fqns:
        registry.register(query_handler_fqn)
