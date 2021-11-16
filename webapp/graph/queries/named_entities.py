from typing import List

from graphene import ObjectType, Field, String
from graphql import ResolveInfo

from news_service_lib.graph.graphql_utils import login_required
from webapp.graph.model import NamedEntitySchema, NamedEntityFilter
from models.named_entity import NamedEntity as NamedEntityModel
from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class NamedEntityQueries(ObjectType):
    named_entities: List[NamedEntitySchema] = AuthenticatedFilterableField(NamedEntitySchema.connection,
                                                                           filters=NamedEntityFilter())
    named_entity: NamedEntitySchema = Field(NamedEntitySchema, value=String())

    @staticmethod
    @login_required
    async def resolve_named_entity(_, info: ResolveInfo, value: str) -> NamedEntityModel:
        query = NamedEntitySchema.get_query(info)
        return query.filter(NamedEntityModel.value == value).one()
