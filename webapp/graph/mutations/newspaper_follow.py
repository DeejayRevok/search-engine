"""
Newspaper follow schema mutations
"""
from graphene import Boolean, String, ObjectType, Mutation
from graphql import ResolveInfo
from news_service_lib.graphql import login_required

from models import Newspaper as NewspaperModel
from services.crud.newspaper_follow_service import NewspaperFollowService
from services.crud.newspaper_service import NewspaperService


class FollowNewspaper(Mutation):
    """
    Mutation to create a newspaper follow
    """
    ok = Boolean(description="True if the association creation was successful, False otherwise")

    class Arguments:
        """
        Mutation arguments
        """
        newspaper_name = String(required=True, description='Name of the newspaper to follow')

    @staticmethod
    @login_required
    async def mutate(_, info, newspaper_name: str):
        """
        Mutation handler which creates the named newspaper follow with the current user

        Args:
            info: mutation resolving info
            newspaper_name: name of the newspaper to follow

        Returns: create mutation

        """
        user_id: int = info.context['request'].user['id']

        newspaper_service: NewspaperService = info.context['request'].app['newspaper_service']
        newspaper_follow_service: NewspaperFollowService = info.context['request'].app['newspaper_follow_service']

        newspaper: NewspaperModel = await newspaper_service.read_one(name=newspaper_name)
        if newspaper:
            await newspaper_follow_service.save(user_id=user_id, newspaper_id=newspaper.id)

            return FollowNewspaper(ok=True)
        else:
            raise ValueError(f'Newspaper {newspaper_name} not found')


class UnfollowNewspaper(Mutation):
    """
    Mutation to delete a newspaper follow
    """
    ok = Boolean(description="True if the association deletion was successful, False otherwise")

    class Arguments:
        """
        Mutation arguments
        """
        new_title = String(required=True, description='Name of the newspaper to unfollow')

    @staticmethod
    @login_required
    async def mutate(_, info: ResolveInfo, newspaper_name: str):
        """
        Mutation handler

        Args:
            info: Resolve information
            newspaper_name: Name of the newspaper to unfollow

        Returns: mutation

        """
        user_id: int = info.context['request'].user['id']

        newspaper_service: NewspaperService = info.context['request'].app['newspaper_service']
        newspaper_follow_service: NewspaperFollowService = info.context['request'].app['newspaper_follow_service']

        newspaper: NewspaperModel = await newspaper_service.read_one(name=newspaper_name)
        if newspaper:
            newspaper_follow = await newspaper_follow_service.read_one(user_id=user_id, new_id=newspaper.id)
            if newspaper_follow:
                await newspaper_follow_service.delete(newspaper_follow.id)
                return UnfollowNewspaper(ok=True)
            else:
                raise ValueError('Newspaper follow not found')
        else:
            raise ValueError(f'Newspaper {newspaper_name} not found')


class NewspaperFollowMutations(ObjectType):
    """
    Newspaper follow GraphQL schema mutations
    """
    follow_newspaper = FollowNewspaper.Field()
    unfollow_newspaper = UnfollowNewspaper.Field()
