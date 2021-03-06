"""
User new schema mutations
"""
from graphene import Boolean, String, ObjectType, Mutation
from graphql import ResolveInfo
from news_service_lib.graphql import login_required

from models import New as NewModel
from services.crud.new_service import NewService
from services.crud.user_new_service import UserNewService


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
        user_new_service: UserNewService = info.context['request'].app['user_new_service']

        new: NewModel = await new_service.read_one(title=new_title)
        if new:
            await user_new_service.save(user_id=user_id, new_id=new.id)

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
        user_new_service: UserNewService = info.context['request'].app['user_new_service']

        new: NewModel = await new_service.read_one(title=new_title)
        if new:
            user_new = await user_new_service.read_one(user_id=user_id, new_id=new.id)
            if user_new:
                await user_new_service.delete(user_new.id)
                return DeleteUserNew(ok=True)
            else:
                raise ValueError('User new association not found')
        else:
            raise ValueError(f'New {new_title} not found')


class UserNewMutations(ObjectType):
    """
    User new GraphQL schema mutations
    """
    create_user_new = CreateUserNew.Field()
    delete_user_new = DeleteUserNew.Field()
