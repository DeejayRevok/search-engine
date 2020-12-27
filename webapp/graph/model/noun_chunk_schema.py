"""
Noun chunk models GraphQL module
"""
from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

from models import NounChunk as NounChunkModel


class NounChunkSchema(SQLAlchemyObjectType):
    """
    GraphQL noun chunk model schema
    """
    class Meta:
        """
        Noun chunk schema metadata
        """
        model = NounChunkModel
        interfaces = (Node,)


class NounChunkFilter(FilterSet):
    """
    GraphQL noun chunk filters schema
    """
    class Meta:
        """
        Noun chunk filter schema metadata
        """
        model = NounChunkModel
        fields = {
            'value': [...],
        }
