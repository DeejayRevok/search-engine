from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType

from models.user import User as UserModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (Node,)
