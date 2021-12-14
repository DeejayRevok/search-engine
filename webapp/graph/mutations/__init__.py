"""
GraphQL mutations module
"""
from webapp.graph.mutations.newspapers import NewspaperMutations
from webapp.graph.mutations.user import UserMutations


class Mutation(NewspaperMutations, UserMutations):
    """
    GraphQL aggregated mutation schema
    """
