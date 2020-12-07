"""
Named entity schema queries
"""
from typing import List

from graphene import ObjectType, Field, String
from graphql import ResolveInfo

from news_service_lib.graphql import login_required
from webapp.graph.model import NamedEntitySchema, NamedEntityFilter
from models import NamedEntity as NamedEntityModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class NamedEntityQueries(ObjectType):
    """
    NamedEntity GraphQL queries definition
    """
    named_entities: List[NamedEntitySchema] = AuthenticatedFilterableField(NamedEntitySchema.connection,
                                                                           filters=NamedEntityFilter())
    named_entity: NamedEntitySchema = Field(NamedEntitySchema, title=String())

    @staticmethod
    @login_required
    async def resolve_named_entity(_, info: ResolveInfo, value: str) -> NamedEntityModel:
        """
        Named entity resolver

        Returns: named entity with the input value

        """
        query = NamedEntitySchema.get_query(info)
        return query.filter(NamedEntityModel.value == value).one()
