"""
GraphQL mutations module
"""
from webapp.graph.mutations.newspaper_follow import NewspaperFollowMutations
from webapp.graph.mutations.newspapers import NewspaperMutations
from webapp.graph.mutations.user_news import UserNewMutations
from webapp.graph.mutations.user_sources import UserSourceMutations


class Mutation(NewspaperMutations,
               UserSourceMutations,
               UserNewMutations,
               NewspaperFollowMutations):
    """
    GraphQL aggregated mutation schema
    """