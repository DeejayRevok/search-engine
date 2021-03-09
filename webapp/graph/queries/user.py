"""
User schema queries
"""
from graphene import ObjectType, Field
from graphql import ResolveInfo
from news_service_lib.graphql import login_required

from models import User as UserModel
from webapp.graph.model import User


class UserQueries(ObjectType):
    """
    User GraphQL queries definition
    """
    user: User = Field(User)

    @staticmethod
    @login_required
    async def resolve_user(_, info: ResolveInfo) -> UserModel:
        """
        User query resolver

        Returns: logged user data

        """
        user_id: int = info.context['request'].user['id']

        query = User.get_query(info)
        return query.filter(UserModel.id == user_id).one()
