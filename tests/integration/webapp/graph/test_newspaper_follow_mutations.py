from logging import getLogger
from unittest import TestCase

from aiohttp.web_app import Application
from aiounittest import async_test
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor
import nest_asyncio

from infrastructure.repositories.newspaper_repository import NewspaperRepository
from infrastructure.repositories.user_repository import UserRepository
from models.base import BASE
from models.newspaper import Newspaper
from models.user import User
from news_service_lib.storage.sql.engine_type import SqlEngineType
from news_service_lib.storage.sql.session_provider import SqlSessionProvider
from news_service_lib.storage.sql.utils import create_sql_engine
from webapp.container_config import container
from webapp.graph import schema

nest_asyncio.apply()


class MockRequest:
    def __init__(self, user, app):
        self.user = user
        self.app = app


class TestNewspaperFollowMutations(TestCase):
    USER_ID = 1
    TEST_NEWSPAPER = "test_newspaper"
    FOLLOW_NEWSPAPER_MUTATION = """
                mutation FollowNewspaper($name: String!){
                    followNewspaper(newspaperName: $name){
                        ok
                    }
                }
            """

    UNFOLLOW_NEWSPAPER_MUTATION = """
                    mutation UnfollowNewspaper($name: String!){
                        unfollowNewspaper(newspaperName: $name){
                            ok
                        }
                    }
                """

    def setUp(self) -> None:
        container.reset()
        test_engine = create_sql_engine(SqlEngineType.SQLITE)
        self.session_provider = SqlSessionProvider(test_engine)
        BASE.query = self.session_provider.query_property
        BASE.metadata.bind = test_engine
        BASE.metadata.create_all()
        logger = getLogger()

        self.newspaper_repository = NewspaperRepository(self.session_provider, logger)
        self.user_repository = UserRepository(self.session_provider, logger)

        app = Application()
        container.set("session_provider", self.session_provider)
        container.set("newspaper_repository", self.newspaper_repository)
        container.set("user_repository", self.user_repository)
        self.app = app

    @async_test
    async def test_follow_newspaper_success(self):
        await self.user_repository.save(User(id=2, username="test2"))
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        await self.newspaper_repository.save(Newspaper(name=self.TEST_NEWSPAPER, user_id=2))
        client = Client(schema)
        client.execute(
            self.FOLLOW_NEWSPAPER_MUTATION,
            variable_values={"name": self.TEST_NEWSPAPER},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=AsyncioExecutor(),
        )
        with self.session_provider():
            newspaper = await self.newspaper_repository.get_one_filtered(name=self.TEST_NEWSPAPER)
            self.assertTrue(len(newspaper.follows))

    @async_test
    async def test_follow_newspaper_same_user(self):
        await self.user_repository.save(User(id=2, username="test2"))
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        await self.newspaper_repository.save(Newspaper(name=self.TEST_NEWSPAPER, user_id=self.USER_ID))
        client = Client(schema)
        response = client.execute(
            self.FOLLOW_NEWSPAPER_MUTATION,
            variable_values={"name": self.TEST_NEWSPAPER},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=AsyncioExecutor(),
        )
        self.assertIn("errors", response)
        self.assertGreater(len(response["errors"]), 0)

    @async_test
    async def test_follow_unexisting_newspaper(self):
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        client = Client(schema)
        response = client.execute(
            self.FOLLOW_NEWSPAPER_MUTATION,
            variable_values={"name": "unexisting_newspaper"},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=AsyncioExecutor(),
        )
        self.assertIn("errors", response)
        self.assertGreater(len(response["errors"]), 0)

    @async_test
    async def test_unfollow_newspaper(self):
        await self.user_repository.save(User(id=2, username="test2"))
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        await self.newspaper_repository.save(Newspaper(name=self.TEST_NEWSPAPER, user_id=2))
        client = Client(schema)
        executor = AsyncioExecutor()
        client.execute(
            self.FOLLOW_NEWSPAPER_MUTATION,
            variable_values={"name": self.TEST_NEWSPAPER},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=executor,
        )
        with self.session_provider():
            newspaper = await self.newspaper_repository.get_one_filtered(name=self.TEST_NEWSPAPER)
            self.assertTrue(len(newspaper.follows))
        client.execute(
            self.UNFOLLOW_NEWSPAPER_MUTATION,
            variable_values={"name": self.TEST_NEWSPAPER},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=executor,
        )
        with self.session_provider():
            newspaper = await self.newspaper_repository.get_one_filtered(name=self.TEST_NEWSPAPER)
            self.assertFalse(len(newspaper.follows))

    @async_test
    async def test_unfollow_not_followed_newspaper(self):
        await self.user_repository.save(User(id=2, username="test2"))
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        await self.newspaper_repository.save(Newspaper(name=self.TEST_NEWSPAPER, user_id=2))
        client = Client(schema)
        executor = AsyncioExecutor()
        response = client.execute(
            self.UNFOLLOW_NEWSPAPER_MUTATION,
            variable_values={"name": self.TEST_NEWSPAPER},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=executor,
        )
        self.assertIn("errors", response)
        self.assertGreater(len(response["errors"]), 0)
