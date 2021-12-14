from typing import List

from graphene import ObjectType, Field, String
from graphql import ResolveInfo

from news_service_lib.graph.graphql_utils import login_required
from webapp.graph.model import NounChunkSchema, NounChunkFilter
from models.noun_chunk import NounChunk as NounChunkModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class NounChunkQueries(ObjectType):
    noun_chunks: List[NounChunkSchema] = AuthenticatedFilterableField(
        NounChunkSchema.connection, filters=NounChunkFilter()
    )
    noun_chunk: NounChunkSchema = Field(NounChunkSchema, value=String())

    @staticmethod
    @login_required
    async def resolve_noun_chunk(_, info: ResolveInfo, value: str) -> NounChunkModel:
        query = NounChunkSchema.get_query(info)
        return query.filter(NounChunkModel.value == value).one()
