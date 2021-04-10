"""
New like mutations tests module
"""
from unittest import TestCase

from aiohttp.web_app import Application
from aiounittest import async_test
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor
import nest_asyncio

from news_service_lib.storage.sql import create_sql_engine, SqlEngineType, SqlSessionProvider, init_sql_db

from models import BASE
from services.crud.new_service import NewService
from services.crud.source_service import SourceService
from services.crud.user_service import UserService
from webapp.container_config import container
from webapp.graph import schema

nest_asyncio.apply()


class MockRequest:
    """
    Mocked request used for testing purposes
    """
    def __init__(self, user, app):
        self.user = user
        self.app = app


class TestNewLikeMutations(TestCase):
    """
    New like mutations test cases implementation
    """
    USER_ID = 1
    TEST_NEW = 'test_new'
    LIKE_NEW_MUTATION = '''
                mutation LikeNew($title: String!){
                    likeNew(newTitle: $title){
                        ok
                    }
                }
            '''

    DELETE_LIKE_MUTATION = '''
                    mutation DeleteLikeNew($title: String!){
                        deleteNewLike(newTitle: $title){
                            ok
                        }
                    }
                '''

    def setUp(self) -> None:
        """
        Set up the test environment creating the database engine
        """
        container.reset()
        test_engine = create_sql_engine(SqlEngineType.SQLITE)
        self.session_provider = SqlSessionProvider(test_engine)
        BASE.query = self.session_provider.query_property
        init_sql_db(BASE, test_engine)

        self.new_service = NewService(session_provider=self.session_provider)
        self.user_service = UserService(session_provider=self.session_provider)
        self.source_service = SourceService(session_provider=self.session_provider)

        app = Application()
        container.set('session_provider', self.session_provider)
        container.set('new_service', self.new_service)
        container.set('user_service', self.user_service)
        self.app = app

    @async_test
    async def test_like_new_success(self):
        """
        Test the like new mutation stores the like
        """
        await self.source_service.save(name='test_source')
        await self.user_service.save(id=self.USER_ID, username='test')
        await self.new_service.save(title=self.TEST_NEW, url='test_url', sentiment=0.0,
                                    source_id=1)
        client = Client(schema)
        client.execute(self.LIKE_NEW_MUTATION,
                       variable_values={
                         'title': self.TEST_NEW
                       },
                       context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                       executor=AsyncioExecutor())
        with self.session_provider():
            new = await self.new_service.read_one(title=self.TEST_NEW)
            self.assertTrue(len(new.likes))

    @async_test
    async def test_like_unexisting_new(self):
        """
        Test liking an unexisting new returns error
        """
        await self.user_service.save(id=self.USER_ID, username='test')
        client = Client(schema)
        response = client.execute(self.LIKE_NEW_MUTATION,
                                  variable_values={
                                     'title': 'unexisting_new'
                                  },
                                  context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                                  executor=AsyncioExecutor())
        self.assertIn('errors', response)
        self.assertGreater(len(response['errors']), 0)

    @async_test
    async def test_delete_new_like(self):
        """
        Test deleting a new like deletes it
        """
        await self.source_service.save(name='test_source')
        await self.user_service.save(id=self.USER_ID, username='test')
        await self.new_service.save(title=self.TEST_NEW, url='test_url', sentiment=0.0,
                                    source_id=1)
        client = Client(schema)
        executor = AsyncioExecutor()
        client.execute(self.LIKE_NEW_MUTATION,
                       variable_values={
                           'title': self.TEST_NEW
                       },
                       context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                       executor=executor)
        with self.session_provider():
            new = await self.new_service.read_one(title=self.TEST_NEW)
            self.assertTrue(len(new.likes))
        client.execute(self.DELETE_LIKE_MUTATION,
                       variable_values={
                           'title': self.TEST_NEW
                       },
                       context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                       executor=executor)
        with self.session_provider():
            new = await self.new_service.read_one(title=self.TEST_NEW)
            self.assertFalse(len(new.likes))

    @async_test
    async def test_deleting_like_not_created(self):
        """
        Test deleting a like from a new not liked yet returns error
        """
        await self.user_service.save(id=self.USER_ID, username='test')
        client = Client(schema)
        executor = AsyncioExecutor()
        response = client.execute(self.DELETE_LIKE_MUTATION,
                                  variable_values={
                                       'title': self.TEST_NEW
                                  },
                                  context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                                  executor=executor)
        self.assertIn('errors', response)
        self.assertGreater(len(response['errors']), 0)
