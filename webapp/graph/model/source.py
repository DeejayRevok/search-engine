"""
Source model GraphQL module
"""
from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

from models import Source as SourceModel


class Source(SQLAlchemyObjectType):
    """
    GraphQL source model schema
    """
    class Meta:
        """
        Source model schema metadata
        """
        model = SourceModel
        interfaces = (Node,)


class SourceFilter(FilterSet):
    """
    GraphQL source filters schema
    """
    class Meta:
        """
        Source filter schema metadata
        """
        model = SourceModel
        fields = {
            'name': [...]
        }
