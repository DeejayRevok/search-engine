"""
GraphQL queries entry point
"""
from webapp.graph.queries.named_entities import NamedEntityQueries
from webapp.graph.queries.named_entity_types import NamedEntityTypeQueries
from webapp.graph.queries.news import NewQueries
from webapp.graph.queries.newspapers import NewspaperQueries
from webapp.graph.queries.noun_chunks import NounChunkQueries
from webapp.graph.queries.sources import SourceQueries
from webapp.graph.queries.user import UserQueries


class Query(NewQueries,
            SourceQueries,
            NamedEntityQueries,
            NamedEntityTypeQueries,
            NounChunkQueries,
            NewspaperQueries,
            UserQueries):
    """
    The main GraphQL query point.
    """
