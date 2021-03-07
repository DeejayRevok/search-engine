"""
Newspaper follow model graphQL schema
"""
from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import NewspaperFollow as NewspaperFollowModel


class NewspaperFollow(SQLAlchemyObjectType):
    """
    GraphQL newspaper follow model schema
    """
    class Meta:
        """
        Newspaper follow schema metadata
        """
        model = NewspaperFollowModel
        interfaces = (Node,)
