"""
Newspaper schema queries
"""
from typing import List

from graphene import ObjectType, Field, String, List as GraphList
from graphql import ResolveInfo
from news_service_lib.graphql import login_required

from webapp.graph.model.newspaper import Newspaper, NewspaperFilter
from models import Newspaper as NewspaperModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class NewspaperQueries(ObjectType):
    """
    Newspaper GraphQL queries definition
    """
    newspapers: List[Newspaper] = AuthenticatedFilterableField(Newspaper.connection, filters=NewspaperFilter())
    user_newspapers: List[Newspaper] = GraphList(Newspaper)
    newspaper: Newspaper = Field(Newspaper, name=String())

    @staticmethod
    @login_required
    async def resolve_user_newspapers(_, info: ResolveInfo) -> List[Newspaper]:
        """
        Uer newspapers resolver

        Returns: user newspapers

        """
        user_id: int = info.context['request'].user['id']

        query = Newspaper.get_query(info)
        return list(query.filter(NewspaperModel.user_id == user_id))

    @staticmethod
    @login_required
    async def resolve_newspaper(_, info: ResolveInfo, name: str) -> Newspaper:
        """
        Newspaper resolver

        Returns: newspaper with the input value

        """
        query = Newspaper.get_query(info)
        return query.filter(NewspaperModel.name == name).one()
