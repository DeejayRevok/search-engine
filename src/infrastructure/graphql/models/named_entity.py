from graphene import ObjectType, String, Field

from infrastructure.graphql.models.named_entity_type import NamedEntityType


class NamedEntity(ObjectType):
    value = String(description="Named entity value")
    named_entity_type = Field(NamedEntityType)
