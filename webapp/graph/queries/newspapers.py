from typing import List

from graphene import ObjectType, Field, String
from graphql import ResolveInfo
from news_service_lib.graph.graphql_utils import login_required

from webapp.graph.model.newspaper import Newspaper, NewspaperFilter
from models.newspaper import Newspaper as NewspaperModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class NewspaperQueries(ObjectType):
    newspapers: List[Newspaper] = AuthenticatedFilterableField(Newspaper.connection, filters=NewspaperFilter())
    newspaper: Newspaper = Field(Newspaper, name=String())

    @staticmethod
    @login_required
    async def resolve_newspaper(_, info: ResolveInfo, name: str) -> Newspaper:
        query = Newspaper.get_query(info)
        return query.filter(NewspaperModel.name == name).one()
