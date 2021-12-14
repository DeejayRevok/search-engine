from logging import getLogger
from unittest import TestCase

from aiohttp.web_app import Application
from aiounittest import async_test
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor
import nest_asyncio

from infrastructure.repositories.source_repository import SourceRepository
from infrastructure.repositories.user_repository import UserRepository
from models.base import BASE

from models.source import Source
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


class TestNewLikeMutations(TestCase):
    USER_ID = 1
    TEST_SOURCE = "test_source"
    FOLLOW_SOURCE_MUTATION = """
                mutation FollowSource($name: String!){
                    followSource(sourceName: $name){
                        ok
                    }
                }
            """

    UNFOLLOW_SOURCE_MUTATION = """
                    mutation UnfollowSource($name: String!){
                        unfollowSource(sourceName: $name){
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

        self.user_repository = UserRepository(self.session_provider, logger)
        self.source_repository = SourceRepository(self.session_provider, logger)

        app = Application()
        container.set("session_provider", self.session_provider)
        container.set("source_repository", self.source_repository)
        container.set("user_repository", self.user_repository)
        self.app = app

    @async_test
    async def test_follow_source_success(self):
        await self.source_repository.save(Source(name=self.TEST_SOURCE))
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        client = Client(schema)
        client.execute(
            self.FOLLOW_SOURCE_MUTATION,
            variable_values={"name": self.TEST_SOURCE},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=AsyncioExecutor(),
        )
        with self.session_provider():
            source = await self.source_repository.get_one_filtered(name=self.TEST_SOURCE)
            self.assertTrue(len(source.follows))

    @async_test
    async def test_follow_unexisting_source(self):
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        client = Client(schema)
        response = client.execute(
            self.FOLLOW_SOURCE_MUTATION,
            variable_values={"name": "unexisting_source"},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=AsyncioExecutor(),
        )
        self.assertIn("errors", response)
        self.assertGreater(len(response["errors"]), 0)

    @async_test
    async def test_unfollow_source(self):
        await self.source_repository.save(Source(name=self.TEST_SOURCE))
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        client = Client(schema)
        executor = AsyncioExecutor()
        client.execute(
            self.FOLLOW_SOURCE_MUTATION,
            variable_values={"name": self.TEST_SOURCE},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=executor,
        )
        with self.session_provider():
            source = await self.source_repository.get_one_filtered(name=self.TEST_SOURCE)
            self.assertTrue(len(source.follows))
        client.execute(
            self.UNFOLLOW_SOURCE_MUTATION,
            variable_values={"name": self.TEST_SOURCE},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=executor,
        )
        with self.session_provider():
            source = await self.source_repository.get_one_filtered(name=self.TEST_SOURCE)
            self.assertFalse(len(source.follows))

    @async_test
    async def test_unfollow_source_not_followed(self):
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        client = Client(schema)
        executor = AsyncioExecutor()
        response = client.execute(
            self.UNFOLLOW_SOURCE_MUTATION,
            variables={"name": self.TEST_SOURCE},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=executor,
        )
        self.assertIn("errors", response)
        self.assertGreater(len(response["errors"]), 0)
