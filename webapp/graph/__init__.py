"""
GraphQL initialization module
"""
from graphene import Schema

from webapp.graph.mutations import Mutation
from webapp.graph.queries import Query

schema = Schema(query=Query,
                mutation=Mutation)
