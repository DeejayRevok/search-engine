"""
User mutations module
"""
from graphene import Boolean, String, ObjectType, Mutation
from graphql import ResolveInfo

from news_service_lib.graphql import login_required

from models import New as NewModel, User as UserModel, Newspaper as NewspaperModel, Source as SourceModel
from services.crud.new_service import NewService
from services.crud.newspaper_service import NewspaperService
from services.crud.source_service import SourceService
from services.crud.user_service import UserService


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
        user_service: UserService = info.context['request'].app['user_service']

        with info.context['request'].app['session_provider'](read_only=False):
            new: NewModel = await new_service.read_one(title=new_title)
            if new:
                user: UserModel = await user_service.read_one(id=user_id)
                user.new_likes.append(new)
                await user_service.update(user)

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
        user_service: UserService = info.context['request'].app['user_service']

        with info.context['request'].app['session_provider'](read_only=False):
            new: NewModel = await new_service.read_one(title=new_title)
            if new:
                user: UserModel = await user_service.read_one(id=user_id)
                if new in user.new_likes:
                    user.new_likes.remove(new)
                    await user_service.update(user)
                    return DeleteNewLike(ok=True)
                else:
                    raise ValueError(f'New {new_title} not liked yet')
            else:
                raise ValueError(f'New {new_title} not found')


class FollowNewspaper(Mutation):
    """
    Mutation to follow a newspaper
    """
    ok = Boolean(description="True if the follow creation was successful, False otherwise")

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
        user_service: UserService = info.context['request'].app['user_service']

        with info.context['request'].app['session_provider'](read_only=False):
            newspaper: NewspaperModel = await newspaper_service.read_one(name=newspaper_name)
            if newspaper:
                user: UserModel = await user_service.read_one(id=user_id)
                if newspaper.user_id != user_id:
                    user.newspaper_follows.append(newspaper)
                    await user_service.update(user)

                    return FollowNewspaper(ok=True)
                else:
                    raise ValueError(f'Impossible to follow your own newspaper')
            else:
                raise ValueError(f'Newspaper {newspaper_name} not found')


class UnfollowNewspaper(Mutation):
    """
    Mutation to delete a newspaper follow
    """
    ok = Boolean(description="True if the unfollow was successful, False otherwise")

    class Arguments:
        """
        Mutation arguments
        """
        newspaper_name = String(required=True, description='Name of the newspaper to unfollow')

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
        user_service: UserService = info.context['request'].app['user_service']

        with info.context['request'].app['session_provider'](read_only=False):
            newspaper: NewspaperModel = await newspaper_service.read_one(name=newspaper_name)
            if newspaper:
                user: UserModel = await user_service.read_one(id=user_id)
                if newspaper in user.newspaper_follows:
                    user.newspaper_follows.remove(newspaper)
                    await user_service.update(user)
                    return UnfollowNewspaper(ok=True)
                else:
                    raise ValueError('Newspaper not followed yet')
            else:
                raise ValueError(f'Newspaper {newspaper_name} not found')


class FollowSource(Mutation):
    """
    Mutation to follow an existing source
    """
    ok = Boolean(description="True if the source follow was successful, False otherwise")

    class Arguments:
        """
        Mutation arguments
        """
        source_name = String(required=True, description='Name of the source to follow')

    @staticmethod
    @login_required
    async def mutate(_, info, source_name: str):
        """
        Mutation handler which creates the association of the current user with the named source

        Args:
            info: mutation resolving info
            source_name: name of the source to follow

        Returns: create mutation

        """
        user_id: int = info.context['request'].user['id']

        source_service: SourceService = info.context['request'].app['source_service']
        user_service: UserService = info.context['request'].app['user_service']

        with info.context['request'].app['session_provider'](read_only=False):
            source: SourceModel = await source_service.read_one(name=source_name)
            if source:
                user: UserModel = await user_service.read_one(id=user_id)
                user.source_follows.append(source)
                await user_service.update(user)

                return FollowSource(ok=True)
            else:
                raise ValueError(f'Source {source_name} not found')


class UnfollowSource(Mutation):
    """
    Mutation to unfollow a source
    """
    ok = Boolean(description="True if the unfollow was successful, False otherwise")

    class Arguments:
        """
        Mutation arguments
        """
        source_name = String(required=True, description='Name of the source to unfollow')

    @staticmethod
    @login_required
    async def mutate(_, info: ResolveInfo, source_name: str):
        """
        Mutation handler

        Args:
            info: Resolve information
            source_name: Name of the source to unfollow

        Returns: mutation

        """
        user_id: int = info.context['request'].user['id']

        source_service: SourceService = info.context['request'].app['source_service']
        user_service: UserService = info.context['request'].app['user_service']

        with info.context['request'].app['session_provider'](read_only=False):
            source: SourceModel = await source_service.read_one(name=source_name)
            if source:
                user: UserModel = await user_service.read_one(id=user_id)
                if source in user.source_follows:
                    user.source_follows.remove(source)
                    await user_service.update(user)
                    return UnfollowSource(ok=True)
                else:
                    raise ValueError('Source not followed yet')
            else:
                raise ValueError(f'Source {source_name} not found')


class CreateUserNew(Mutation):
    """
    Mutation to create a user new association
    """
    ok = Boolean(description="True if the association creation was successful, False otherwise")

    class Arguments:
        """
        Mutation arguments
        """
        new_title = String(required=True, description='Title of the new to associate with the user')

    @staticmethod
    @login_required
    async def mutate(_, info, new_title: str):
        """
        Mutation handler which creates the association of the current user with the new specified

        Args:
            info: mutation resolving info
            new_title: associated new title

        Returns: create mutation

        """
        user_id: int = info.context['request'].user['id']

        new_service: NewService = info.context['request'].app['new_service']
        user_service: UserService = info.context['request'].app['user_service']

        with info.context['request'].app['session_provider'](read_only=False):
            new: NewModel = await new_service.read_one(title=new_title)
            if new:
                user: UserModel = await user_service.read_one(id=user_id)
                user.news.append(new)
                await user_service.update(user)

                return CreateUserNew(ok=True)
            else:
                raise ValueError(f'New {new_title} not found')


class DeleteUserNew(Mutation):
    """
    Mutation to delete a user new
    """
    ok = Boolean(description="True if the association deletion was successful, False otherwise")

    class Arguments:
        """
        Mutation arguments
        """
        new_title = String(required=True, description='Title of the new association to delete')

    @staticmethod
    @login_required
    async def mutate(_, info: ResolveInfo, new_title: str):
        """
        Mutation handler

        Args:
            info: Resolve information
            new_title: Title of the new to remove association

        Returns: mutation

        """
        user_id: int = info.context['request'].user['id']

        new_service: NewService = info.context['request'].app['new_service']
        user_service: UserService = info.context['request'].app['user_service']

        with info.context['request'].app['session_provider'](read_only=False):
            new: NewModel = await new_service.read_one(title=new_title)
            if new:
                user: UserModel = await user_service.read_one(id=user_id)
                if new in user.news:
                    user.news.remove(new)
                    await user_service.update(user)
                    return DeleteUserNew(ok=True)
                else:
                    raise ValueError('User new association not found')
            else:
                raise ValueError(f'New {new_title} not found')


class UserMutations(ObjectType):
    """
    User GraphQL schema mutations
    """
    like_new = LikeNew.Field()
    delete_new_like = DeleteNewLike.Field()

    follow_newspaper = FollowNewspaper.Field()
    unfollow_newspaper = UnfollowNewspaper.Field()

    follow_source = FollowSource.Field()
    unfollow_source = UnfollowSource.Field()

    create_user_new = CreateUserNew.Field()
    delete_user_new = DeleteUserNew.Field()
