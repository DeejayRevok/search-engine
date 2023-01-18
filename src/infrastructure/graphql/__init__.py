from graphene import Schema
from pypendency.builder import container_builder

from infrastructure.graphql.mutations import Mutations
from infrastructure.graphql.queries import Queries


def load() -> None:
    schema = Schema(query=Queries, mutation=Mutations)
    container_builder.set("graphene.Schema", schema)
