from __future__ import annotations
from typing import List

from graphene import ObjectType, Field, String
from graphql import ResolveInfo

from news_service_lib.graph.graphql_utils import login_required
from webapp.graph.model import NewSchema, NewFilter, NewsSearch
from models.new import New as NewModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class NewQueries(ObjectType):
    news: List[NewSchema] = AuthenticatedFilterableField(NewSchema.connection, filters=NewFilter())
    new: NewSchema = Field(NewSchema, title=String())
    news_search: NewsSearch = Field(NewsSearch)

    @staticmethod
    @login_required
    async def resolve_new(_, info: ResolveInfo, title: str) -> NewModel:
        query = NewSchema.get_query(info)
        return query.filter(NewModel.title == title).one()

    @staticmethod
    @login_required
    async def resolve_news_search(_, __) -> NewsSearch:
        return NewsSearch(result=[])
