from graphene import ObjectType, Field
from graphql import ResolveInfo
from news_service_lib.graph.graphql_utils import login_required

from models.user import User as UserModel
from webapp.graph.model import User


class UserQueries(ObjectType):
    user: User = Field(User)

    @staticmethod
    @login_required
    async def resolve_user(_, info: ResolveInfo) -> UserModel:
        user_id: int = info.context['request'].user['id']

        query = User.get_query(info)
        return query.filter(UserModel.id == user_id).one()
