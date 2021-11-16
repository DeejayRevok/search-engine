from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

from models.named_entity_type import NamedEntityType as NamedEntityTypeModel


class NamedEntityType(SQLAlchemyObjectType):
    class Meta:
        model = NamedEntityTypeModel
        interfaces = (Node,)


class NamedEntityTypeFilter(FilterSet):
    class Meta:
        model = NamedEntityTypeModel
        fields = {
            'name': [...],
            'description': [...]
        }
