"""
New like model graphQL schema
"""
from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import NewLike as NewLikeModel


class NewLike(SQLAlchemyObjectType):
    """
    GraphQL new like model schema
    """
    class Meta:
        """
        New like schema metadata
        """
        model = NewLikeModel
        interfaces = (Node,)
