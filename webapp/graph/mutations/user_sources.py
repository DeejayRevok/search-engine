"""
User source schema mutations
"""
from graphene import Boolean, String, ObjectType, Mutation
from graphql import ResolveInfo
from news_service_lib.graphql import login_required

from models import Source as SourceModel
from services.crud.source_service import SourceService
from services.crud.user_source_service import UserSourceService


class CreateUserSource(Mutation):
    """
    Mutation to create a user source association
    """
    ok = Boolean(description="True if the association creation was successful, False otherwise")

    class Arguments(object):
        """
        Mutation arguments
        """
        source_name = String(required=True, description='Name of the source to associate with the user')

    @staticmethod
    @login_required
    async def mutate(_, info, source_name: str):
        """
        Mutation handler which creates the association of the current user with the named source

        Args:
            info: mutation resolving info
            source_name: associated source name

        Returns: create mutation

        """
        user_id: int = info.context['request'].user['id']

        source_service: SourceService = info.context['request'].app['source_service']
        user_source_service: UserSourceService = info.context['request'].app['user_source_service']

        source: SourceModel = await source_service.read_one(name=source_name)
        if source:
            await user_source_service.save(user_id=user_id, source_id=source.id)

            return CreateUserSource(ok=True)
        else:
            raise ValueError(f'Source {source_name} not found')


class DeleteUserSource(Mutation):
    """
    Mutation to delete a user source
    """
    ok = Boolean(description="True if the association deletion was successful, False otherwise")

    class Arguments(object):
        """
        Mutation arguments
        """
        source_name = String(required=True, description='Name of the source association to delete')

    @staticmethod
    @login_required
    async def mutate(_, info: ResolveInfo, source_name: str):
        """
        Mutation handler

        Args:
            info: Resolve information
            source_name: Name of the source to remove association

        Returns: mutation

        """
        user_id: int = info.context['request'].user['id']

        source_service: SourceService = info.context['request'].app['source_service']
        user_source_service: UserSourceService = info.context['request'].app['user_source_service']

        source: SourceModel = await source_service.read_one(name=source_name)
        if source:
            user_source = await user_source_service.read_one(user_id=user_id, source_id=source.id)
            if user_source:
                await user_source_service.delete(user_source.id)
                return DeleteUserSource(ok=True)
            else:
                raise ValueError('User source association not found')
        else:
            raise ValueError(f'Source {source_name} not found')


class UserSourceMutations(ObjectType):
    """
    User source GraphQL schema mutations
    """
    create_user_source = CreateUserSource.Field()
    delete_user_source = DeleteUserSource.Field()
