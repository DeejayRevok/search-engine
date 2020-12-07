"""
GraphQL queries entry point
"""
from webapp.graph.queries.named_entities import NamedEntityQueries
from webapp.graph.queries.named_entity_types import NamedEntityTypeQueries
from webapp.graph.queries.news import NewQueries
from webapp.graph.queries.sources import SourceQueries


class Query(NewQueries,
            SourceQueries,
            NamedEntityQueries,
            NamedEntityTypeQueries):
    """
    The main GraphQL query point.
    """
