from infrastructure.graphql.queries.named_entity_queries import NamedEntityQueries
from infrastructure.graphql.queries.new_queries import NewQueries
from infrastructure.graphql.queries.newspaper_queries import NewspaperQueries


class Queries(NewQueries, NamedEntityQueries, NewspaperQueries):
    pass
