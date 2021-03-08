"""
User model GraphQL module
"""
from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType

from models.user import User as UserModel


class User(SQLAlchemyObjectType):
    """
    GraphQL user model schema
    """
    class Meta:
        """
        User model schema metadata
        """
        model = UserModel
        interfaces = (Node,)
