from bus_station.query_terminal.registry.query_registry import QueryRegistry
from pypendency.builder import container_builder


def register() -> None:
    registry: QueryRegistry = container_builder.get(
        "bus_station.query_terminal.registry.in_memory_query_registry.InMemoryQueryRegistry"
    )
    query_handler_fqns = [
        "application.get_named_entities.get_named_entities_query_handler.GetNamedEntitiesQueryHandler",
        "application.get_new.get_new_query_handler.GetNewQueryHandler",
        "application.get_news.get_news_query_handler.GetNewsQueryHandler",
        "application.get_newspapers.get_newspapers_query_handler.GetNewspapersQueryHandler"
    ]

    for query_handler_fqn in query_handler_fqns:
        handler = container_builder.get(query_handler_fqn)
        registry.register(handler, handler)
