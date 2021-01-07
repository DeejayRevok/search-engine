"""
Source schema queries
"""
from typing import List

from graphene import ObjectType, Field, String, List as GraphList
from graphql import ResolveInfo
from news_service_lib.graphql import login_required

from models import Source as SourceModel, UserSource as UserSourceModel
from webapp.graph.model import SourceFilter, Source, UserSource
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class SourceQueries(ObjectType):
    """
    Source GraphQL queries definition
    """
    sources: List[Source] = AuthenticatedFilterableField(Source.connection, filters=SourceFilter())
    user_sources: List[Source] = GraphList(Source)
    source: Source = Field(Source, name=String())

    @staticmethod
    @login_required
    async def resolve_user_sources(_, info: ResolveInfo) -> List[SourceModel]:
        """
        User sources query resolver

        Returns: sources of the authenticated user

        """
        user_id: int = info.context['request'].user['id']

        query = UserSource.get_query(info)
        return [user_source.source for user_source in query.filter(UserSourceModel.user_id == user_id)]

    @staticmethod
    @login_required
    async def resolve_source(_, info: ResolveInfo, name: str) -> SourceModel:
        """
        Source query resolver

        Returns: source identified by the input name

        """
        query = Source.get_query(info)
        return query.filter(SourceModel.name == name).one()
