"""
New like schema mutations
"""
from graphene import Boolean, String, ObjectType, Mutation
from graphql import ResolveInfo
from news_service_lib.graphql import login_required

from models import New as NewModel
from services.crud.new_like_service import NewLikeService
from services.crud.new_service import NewService


class LikeNew(Mutation):
    """
    Mutation to like a new
    """
    ok = Boolean(description="True if the like creation was successful, False otherwise")

    class Arguments:
        """
        Mutation arguments
        """
        new_title = String(required=True, description='Title of the new to like')

    @staticmethod
    @login_required
    async def mutate(_, info, new_title: str):
        """
        Mutation handler which likes the new specified

        Args:
            info: mutation resolving info
            new_title: associated new title

        Returns: create mutation

        """
        user_id: int = info.context['request'].user['id']

        new_service: NewService = info.context['request'].app['new_service']
        new_like_service: NewLikeService = info.context['request'].app['new_like_service']

        new: NewModel = await new_service.read_one(title=new_title)
        if new:
            await new_like_service.save(user_id=user_id, new_id=new.id)

            return LikeNew(ok=True)
        else:
            raise ValueError(f'New {new_title} not found')


class DeleteNewLike(Mutation):
    """
    Mutation to delete a new like
    """
    ok = Boolean(description="True if the like deletion was successful, False otherwise")

    class Arguments:
        """
        Mutation arguments
        """
        new_title = String(required=True, description='Title of the new to delete like')

    @staticmethod
    @login_required
    async def mutate(_, info: ResolveInfo, new_title: str):
        """
        Mutation handler

        Args:
            info: Resolve information
            new_title: Title of the new to remove like

        Returns: mutation

        """
        user_id: int = info.context['request'].user['id']

        new_service: NewService = info.context['request'].app['new_service']
        new_like_service: NewLikeService = info.context['request'].app['new_like_service']

        new: NewModel = await new_service.read_one(title=new_title)
        if new:
            new_like = await new_like_service.read_one(user_id=user_id, new_id=new.id)
            if new_like:
                await new_like_service.delete(new_like.id)
                return DeleteNewLike(ok=True)
            else:
                raise ValueError('New like not found')
        else:
            raise ValueError(f'New {new_title} not found')


class NewLikeMutations(ObjectType):
    """
    New like GraphQL schema mutations
    """
    like_new = LikeNew.Field()
    delete_new_like = DeleteNewLike.Field()
