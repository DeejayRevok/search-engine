"""
New schema queries
"""
from typing import List

from graphene import ObjectType, Field, String
from graphql import ResolveInfo

from news_service_lib.graphql import login_required
from webapp.graph.model import NewSchema, NewFilter
from models import New as NewModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class NewQueries(ObjectType):
    """
    New GraphQL queries definition
    """
    news: List[NewSchema] = AuthenticatedFilterableField(NewSchema.connection, filters=NewFilter())
    new: NewSchema = Field(NewSchema, title=String())

    @staticmethod
    @login_required
    async def resolve_new(_, info: ResolveInfo, title: str) -> NewModel:
        """
        New query resolver

        Returns: new identified by the input title

        """
        query = NewSchema.get_query(info)
        return query.filter(NewModel.title == title).one()
