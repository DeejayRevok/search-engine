"""
GraphQL mutations module
"""
from webapp.graph.mutations.newspapers import NewspaperMutations


class Mutation(NewspaperMutations):
    """
    GraphQL aggregated mutation schema
    """