from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

from models.named_entity import NamedEntity as NamedEntityModel


class NamedEntitySchema(SQLAlchemyObjectType):
    class Meta:
        model = NamedEntityModel
        interfaces = (Node,)
        exclude_fields = ('named_entity_type_id',)


class NamedEntityFilter(FilterSet):
    class Meta:
        model = NamedEntityModel
        fields = {
            'value': [...],
        }
