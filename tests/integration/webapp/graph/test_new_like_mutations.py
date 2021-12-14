from logging import getLogger
from unittest import TestCase

from aiohttp.web_app import Application
from aiounittest import async_test
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor
import nest_asyncio

from infrastructure.repositories.new_repository import NewRepository
from infrastructure.repositories.source_repository import SourceRepository
from infrastructure.repositories.user_repository import UserRepository
from models.base import BASE
from models.new import New
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
    TEST_NEW = "test_new"
    LIKE_NEW_MUTATION = """
                mutation LikeNew($title: String!){
                    likeNew(newTitle: $title){
                        ok
                    }
                }
            """

    DELETE_LIKE_MUTATION = """
                    mutation DeleteLikeNew($title: String!){
                        deleteNewLike(newTitle: $title){
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

        self.new_repository = NewRepository(self.session_provider, logger)
        self.user_repository = UserRepository(self.session_provider, logger)
        self.source_repository = SourceRepository(self.session_provider, logger)

        app = Application()
        container.set("session_provider", self.session_provider)
        container.set("new_repository", self.new_repository)
        container.set("user_repository", self.user_repository)
        self.app = app

    @async_test
    async def test_like_new_success(self):
        await self.source_repository.save(Source(name="test_source"))
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        await self.new_repository.save(New(title=self.TEST_NEW, url="test_url", sentiment=0.0, source_id=1))
        client = Client(schema)
        client.execute(
            self.LIKE_NEW_MUTATION,
            variable_values={"title": self.TEST_NEW},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=AsyncioExecutor(),
        )
        with self.session_provider():
            new = await self.new_repository.get_one_filtered(title=self.TEST_NEW)
            self.assertTrue(len(new.likes))

    @async_test
    async def test_like_unexisting_new(self):
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        client = Client(schema)
        response = client.execute(
            self.LIKE_NEW_MUTATION,
            variable_values={"title": "unexisting_new"},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=AsyncioExecutor(),
        )
        self.assertIn("errors", response)
        self.assertGreater(len(response["errors"]), 0)

    @async_test
    async def test_delete_new_like(self):
        await self.source_repository.save(Source(name="test_source"))
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        await self.new_repository.save(New(title=self.TEST_NEW, url="test_url", sentiment=0.0, source_id=1))
        client = Client(schema)
        executor = AsyncioExecutor()
        client.execute(
            self.LIKE_NEW_MUTATION,
            variable_values={"title": self.TEST_NEW},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=executor,
        )
        with self.session_provider():
            new = await self.new_repository.get_one_filtered(title=self.TEST_NEW)
            self.assertTrue(len(new.likes))
        client.execute(
            self.DELETE_LIKE_MUTATION,
            variable_values={"title": self.TEST_NEW},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=executor,
        )
        with self.session_provider():
            new = await self.new_repository.get_one_filtered(title=self.TEST_NEW)
            self.assertFalse(len(new.likes))

    @async_test
    async def test_deleting_like_not_created(self):
        await self.user_repository.save(User(id=self.USER_ID, username="test"))
        client = Client(schema)
        executor = AsyncioExecutor()
        response = client.execute(
            self.DELETE_LIKE_MUTATION,
            variable_values={"title": self.TEST_NEW},
            context_value={"request": MockRequest({"id": self.USER_ID}, self.app)},
            executor=executor,
        )
        self.assertIn("errors", response)
        self.assertGreater(len(response["errors"]), 0)
