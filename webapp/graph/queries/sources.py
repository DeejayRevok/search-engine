from typing import List

from graphene import ObjectType, Field, String
from graphql import ResolveInfo
from news_service_lib.graph.graphql_utils import login_required

from models.source import Source as SourceModel
from webapp.graph.model import SourceFilter, Source
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class SourceQueries(ObjectType):
    sources: List[Source] = AuthenticatedFilterableField(Source.connection, filters=SourceFilter())
    source: Source = Field(Source, name=String())

    @staticmethod
    @login_required
    async def resolve_source(_, info: ResolveInfo, name: str) -> SourceModel:
        query = Source.get_query(info)
        return query.filter(SourceModel.name == name).one()
