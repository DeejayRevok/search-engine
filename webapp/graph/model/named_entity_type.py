"""
Named entity type models GraphQL module
"""
from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

from models import NamedEntityType as NamedEntityTypeModel


class NamedEntityType(SQLAlchemyObjectType):
    """
    GraphQL named entity type model schema
    """
    class Meta(object):
        """
        Named entity type schema metadata
        """
        model = NamedEntityTypeModel
        interfaces = (Node,)


class NamedEntityTypeFilter(FilterSet):
    """
    GraphQL named entity type filters schema
    """
    class Meta(object):
        """
        Named entity type filter schema metadata
        """
        model = NamedEntityTypeModel
        fields = {
            'name': [...],
            'description': [...]
        }
