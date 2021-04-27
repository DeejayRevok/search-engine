"""
Noun chunk schema queries
"""
from typing import List

from graphene import ObjectType, Field, String
from graphql import ResolveInfo

from news_service_lib.graphql import login_required
from webapp.graph.model import NounChunkSchema, NounChunkFilter
from models import NounChunk as NounChunkModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class NounChunkQueries(ObjectType):
    """
    NounChunk GraphQL queries definition
    """
    noun_chunks: List[NounChunkSchema] = AuthenticatedFilterableField(NounChunkSchema.connection,
                                                                         filters=NounChunkFilter())
    noun_chunk: NounChunkSchema = Field(NounChunkSchema, value=String())

    @staticmethod
    @login_required
    async def resolve_noun_chunk(_, info: ResolveInfo, value: str) -> NounChunkModel:
        """
        Noun chunk resolver

        Returns: noun chunk with the input value

        """
        query = NounChunkSchema.get_query(info)
        return query.filter(NounChunkModel.value == value).one()
