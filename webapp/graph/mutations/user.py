from graphene import Boolean, String, ObjectType, Mutation
from graphql import ResolveInfo

from infrastructure.repositories.new_repository import NewRepository
from infrastructure.repositories.newspaper_repository import NewspaperRepository
from infrastructure.repositories.source_repository import SourceRepository
from infrastructure.repositories.user_repository import UserRepository
from news_service_lib.graph.graphql_utils import login_required

from models.new import New as NewModel
from models.user import User as UserModel
from models.newspaper import Newspaper as NewspaperModel
from models.source import Source as SourceModel
from webapp.container_config import container


class LikeNew(Mutation):
    ok = Boolean(description="True if the like creation was successful, False otherwise")

    class Arguments:
        new_title = String(required=True, description="Title of the new to like")

    @staticmethod
    @login_required
    async def mutate(_, info, new_title: str):
        user_id: int = info.context["request"].user["id"]

        new_repository: NewRepository = container.get("new_repository")
        user_repository: UserRepository = container.get("user_repository")

        with container.get("session_provider")(read_only=False):
            new: NewModel = await new_repository.get_one_filtered(title=new_title)
            if new:
                user: UserModel = await user_repository.get_one_filtered(id=user_id)
                user.new_likes.append(new)
                await user_repository.save(user)

                return LikeNew(ok=True)
            else:
                raise ValueError(f"New {new_title} not found")


class DeleteNewLike(Mutation):
    ok = Boolean(description="True if the like deletion was successful, False otherwise")

    class Arguments:
        new_title = String(required=True, description="Title of the new to delete like")

    @staticmethod
    @login_required
    async def mutate(_, info: ResolveInfo, new_title: str):
        user_id: int = info.context["request"].user["id"]

        new_repository: NewRepository = container.get("new_repository")
        user_repository: UserRepository = container.get("user_repository")

        with container.get("session_provider")(read_only=False):
            new: NewModel = await new_repository.get_one_filtered(title=new_title)
            if new:
                user: UserModel = await user_repository.get_one_filtered(id=user_id)
                if new in user.new_likes:
                    user.new_likes.remove(new)
                    await user_repository.save(user)
                    return DeleteNewLike(ok=True)
                else:
                    raise ValueError(f"New {new_title} not liked yet")
            else:
                raise ValueError(f"New {new_title} not found")


class FollowNewspaper(Mutation):
    ok = Boolean(description="True if the follow creation was successful, False otherwise")

    class Arguments:
        newspaper_name = String(required=True, description="Name of the newspaper to follow")

    @staticmethod
    @login_required
    async def mutate(_, info, newspaper_name: str):
        user_id: int = info.context["request"].user["id"]

        newspaper_repository: NewspaperRepository = container.get("newspaper_repository")
        user_repository: UserRepository = container.get("user_repository")

        with container.get("session_provider")(read_only=False):
            newspaper: NewspaperModel = await newspaper_repository.get_one_filtered(name=newspaper_name)
            if newspaper:
                user: UserModel = await user_repository.get_one_filtered(id=user_id)
                if newspaper.user_id != user_id:
                    user.newspaper_follows.append(newspaper)
                    await user_repository.save(user)

                    return FollowNewspaper(ok=True)
                else:
                    raise ValueError(f"Impossible to follow your own newspaper")
            else:
                raise ValueError(f"Newspaper {newspaper_name} not found")


class UnfollowNewspaper(Mutation):
    ok = Boolean(description="True if the unfollow was successful, False otherwise")

    class Arguments:
        newspaper_name = String(required=True, description="Name of the newspaper to unfollow")

    @staticmethod
    @login_required
    async def mutate(_, info: ResolveInfo, newspaper_name: str):
        user_id: int = info.context["request"].user["id"]

        newspaper_repository: NewspaperRepository = container.get("newspaper_repository")
        user_repository: UserRepository = container.get("user_repository")

        with container.get("session_provider")(read_only=False):
            newspaper: NewspaperModel = await newspaper_repository.get_one_filtered(name=newspaper_name)
            if newspaper:
                user: UserModel = await user_repository.get_one_filtered(id=user_id)
                if newspaper in user.newspaper_follows:
                    user.newspaper_follows.remove(newspaper)
                    await user_repository.save(user)
                    return UnfollowNewspaper(ok=True)
                else:
                    raise ValueError("Newspaper not followed yet")
            else:
                raise ValueError(f"Newspaper {newspaper_name} not found")


class FollowSource(Mutation):
    ok = Boolean(description="True if the source follow was successful, False otherwise")

    class Arguments:
        source_name = String(required=True, description="Name of the source to follow")

    @staticmethod
    @login_required
    async def mutate(_, info, source_name: str):
        user_id: int = info.context["request"].user["id"]

        source_repository: SourceRepository = container.get("source_repository")
        user_repository: UserRepository = container.get("user_repository")

        with container.get("session_provider")(read_only=False):
            source: SourceModel = await source_repository.get_one_filtered(name=source_name)
            if source:
                user: UserModel = await user_repository.get_one_filtered(id=user_id)
                user.source_follows.append(source)
                await user_repository.save(user)

                return FollowSource(ok=True)
            else:
                raise ValueError(f"Source {source_name} not found")


class UnfollowSource(Mutation):
    ok = Boolean(description="True if the unfollow was successful, False otherwise")

    class Arguments:
        source_name = String(required=True, description="Name of the source to unfollow")

    @staticmethod
    @login_required
    async def mutate(_, info: ResolveInfo, source_name: str):
        user_id: int = info.context["request"].user["id"]

        source_repository: SourceRepository = container.get("source_repository")
        user_repository: UserRepository = container.get("user_repository")

        with container.get("session_provider")(read_only=False):
            source: SourceModel = await source_repository.get_one_filtered(name=source_name)
            if source:
                user: UserModel = await user_repository.get_one_filtered(id=user_id)
                if source in user.source_follows:
                    user.source_follows.remove(source)
                    await user_repository.save(user)
                    return UnfollowSource(ok=True)
                else:
                    raise ValueError("Source not followed yet")
            else:
                raise ValueError(f"Source {source_name} not found")


class CreateUserNew(Mutation):
    ok = Boolean(description="True if the association creation was successful, False otherwise")

    class Arguments:
        new_title = String(required=True, description="Title of the new to associate with the user")

    @staticmethod
    @login_required
    async def mutate(_, info, new_title: str):
        user_id: int = info.context["request"].user["id"]

        new_repository: NewRepository = container.get("new_repository")
        user_repository: UserRepository = container.get("user_repository")

        with container.get("session_provider")(read_only=False):
            new: NewModel = await new_repository.get_one_filtered(title=new_title)
            if new:
                user: UserModel = await user_repository.get_one_filtered(id=user_id)
                user.news.append(new)
                await user_repository.save(user)

                return CreateUserNew(ok=True)
            else:
                raise ValueError(f"New {new_title} not found")


class DeleteUserNew(Mutation):
    ok = Boolean(description="True if the association deletion was successful, False otherwise")

    class Arguments:
        new_title = String(required=True, description="Title of the new association to delete")

    @staticmethod
    @login_required
    async def mutate(_, info: ResolveInfo, new_title: str):
        user_id: int = info.context["request"].user["id"]

        new_repository: NewRepository = container.get("new_repository")
        user_repository: UserRepository = container.get("user_repository")

        with container.get("session_provider")(read_only=False):
            new: NewModel = await new_repository.get_one_filtered(title=new_title)
            if new:
                user: UserModel = await user_repository.get_one_filtered(id=user_id)
                if new in user.news:
                    user.news.remove(new)
                    await user_repository.save(user)
                    return DeleteUserNew(ok=True)
                else:
                    raise ValueError("User new association not found")
            else:
                raise ValueError(f"New {new_title} not found")


class UserMutations(ObjectType):
    like_new = LikeNew.Field()
    delete_new_like = DeleteNewLike.Field()

    follow_newspaper = FollowNewspaper.Field()
    unfollow_newspaper = UnfollowNewspaper.Field()

    follow_source = FollowSource.Field()
    unfollow_source = UnfollowSource.Field()

    create_user_new = CreateUserNew.Field()
    delete_user_new = DeleteUserNew.Field()
