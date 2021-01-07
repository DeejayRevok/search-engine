"""
User source model graphQL schema
"""
from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import UserSource as UserSourceModel


class UserSource(SQLAlchemyObjectType):
    """
    GraphQL user source model schema
    """
    class Meta:
        """
        User source schema metadata
        """
        model = UserSourceModel
        interfaces = (Node,)
