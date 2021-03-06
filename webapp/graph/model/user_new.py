"""
User new model graphQL schema
"""
from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import UserNew as UserNewModel


class UserNew(SQLAlchemyObjectType):
    """
    GraphQL user new model schema
    """
    class Meta:
        """
        User new schema metadata
        """
        model = UserNewModel
        interfaces = (Node,)
