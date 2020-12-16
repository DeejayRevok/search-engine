"""
Source schema queries
"""
from typing import List

from graphene import ObjectType, Field, String
from graphql import ResolveInfo

from news_service_lib.graphql import login_required
from webapp.graph.model import SourceFilter, Source
from models import Source as SourceModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class SourceQueries(ObjectType):
    """
    Source GraphQL queries definition
    """
    news: List[Source] = AuthenticatedFilterableField(Source.connection, filters=SourceFilter())
    new: Source = Field(Source, name=String())

    @staticmethod
    @login_required
    async def resolve_source(_, info: ResolveInfo, name: str) -> SourceModel:
        """
        Source query resolver

        Returns: source identified by the input name

        """
        query = Source.get_query(info)
        return query.filter(SourceModel.name == name).one()
