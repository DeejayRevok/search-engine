"""
New schema queries
"""
from __future__ import annotations
from typing import List

from graphene import ObjectType, Field, String, List as GraphList
from graphql import ResolveInfo

from news_service_lib.graphql import login_required
from webapp.graph.model import NewSchema, NewFilter, NewsSearch, UserNew
from models import New as NewModel, UserNew as UserNewModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class NewQueries(ObjectType):
    """
    New GraphQL queries definition
    """
    news: List[NewSchema] = AuthenticatedFilterableField(NewSchema.connection, filters=NewFilter())
    new: NewSchema = Field(NewSchema, title=String())
    news_search: NewsSearch = Field(NewsSearch)
    user_news: List[NewSchema] = GraphList(NewSchema)

    @staticmethod
    @login_required
    async def resolve_user_news(_, info: ResolveInfo) -> List[NewSchema]:
        """
        User news query resolver

        Returns: news related with the authenticated user

        """
        user_id: int = info.context['request'].user['id']

        query = UserNew.get_query(info)
        return [user_new.new for user_new in query.filter(UserNewModel.user_id == user_id)]

    @staticmethod
    @login_required
    async def resolve_new(_, info: ResolveInfo, title: str) -> NewModel:
        """
        New query resolver

        Returns: new identified by the input title

        """
        query = NewSchema.get_query(info)
        return query.filter(NewModel.title == title).one()

    @staticmethod
    @login_required
    async def resolve_news_search(_, __) -> NewsSearch:
        """
        News search query resolver

        Returns: news advanced search proxy

        """
        return NewsSearch(result=[])
