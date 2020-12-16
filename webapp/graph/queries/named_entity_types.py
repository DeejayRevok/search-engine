"""
Named entity type schema queries
"""
from typing import List

from graphene import ObjectType, Field, String
from graphql import ResolveInfo

from news_service_lib.graphql import login_required
from webapp.graph.model import NamedEntityType, NamedEntityTypeFilter
from models import NamedEntityType as NamedEntityTypeModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class NamedEntityTypeQueries(ObjectType):
    """
    NamedEntityType GraphQL queries definition
    """
    named_entity_types: List[NamedEntityType] = AuthenticatedFilterableField(NamedEntityType.connection,
                                                                             filters=NamedEntityTypeFilter())
    named_entity_type: NamedEntityType = Field(NamedEntityType, name=String())

    @staticmethod
    @login_required
    async def resolve_named_entity_type(_, info: ResolveInfo, name: str) -> NamedEntityTypeModel:
        """
        Named entity type query resolver

        Returns: named entity type identified by the input name

        """
        query = NamedEntityType.get_query(info)
        return query.filter(NamedEntityTypeModel.name == name).one()
