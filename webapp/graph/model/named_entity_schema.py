"""
Named entity models GraphQL module
"""
from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

from models import NamedEntity as NamedEntityModel


class NamedEntitySchema(SQLAlchemyObjectType):
    """
    GraphQL named entity model schema
    """
    class Meta:
        """
        Named entity schema metadata
        """
        model = NamedEntityModel
        interfaces = (Node,)
        exclude_fields = ('named_entity_type_id',)


class NamedEntityFilter(FilterSet):
    """
    GraphQL named entity filters schema
    """
    class Meta:
        """
        Named entity filter schema metadata
        """
        model = NamedEntityModel
        fields = {
            'value': [...],
        }
