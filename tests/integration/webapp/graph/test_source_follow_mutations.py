"""
Source follow mutations tests module
"""
from unittest import TestCase

from aiohttp.web_app import Application
from aiounittest import async_test
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor
import nest_asyncio

from news_service_lib.storage.sql import create_sql_engine, SqlEngineType, SqlSessionProvider, init_sql_db

from models import BASE
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
    Source follow mutations test cases implementation
    """
    USER_ID = 1
    TEST_SOURCE = 'test_source'
    FOLLOW_SOURCE_MUTATION = '''
                mutation FollowSource($name: String!){
                    followSource(sourceName: $name){
                        ok
                    }
                }
            '''

    UNFOLLOW_SOURCE_MUTATION = '''
                    mutation UnfollowSource($name: String!){
                        unfollowSource(sourceName: $name){
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

        self.user_service = UserService(session_provider=self.session_provider)
        self.source_service = SourceService(session_provider=self.session_provider)

        app = Application()
        container.set('session_provider', self.session_provider)
        container.set('source_service', self.source_service)
        container.set('user_service', self.user_service)
        self.app = app

    @async_test
    async def test_follow_source_success(self):
        """
        Test the follow source mutation stores the source
        """
        await self.source_service.save(name=self.TEST_SOURCE)
        await self.user_service.save(id=self.USER_ID, username='test')
        client = Client(schema)
        client.execute(self.FOLLOW_SOURCE_MUTATION,
                       variable_values={
                         'name': self.TEST_SOURCE
                       },
                       context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                       executor=AsyncioExecutor())
        with self.session_provider():
            source = await self.source_service.read_one(name=self.TEST_SOURCE)
            self.assertTrue(len(source.follows))

    @async_test
    async def test_follow_unexisting_source(self):
        """
        Test following an unexisting source returns error
        """
        await self.user_service.save(id=self.USER_ID, username='test')
        client = Client(schema)
        response = client.execute(self.FOLLOW_SOURCE_MUTATION,
                                  variable_values={
                                     'name': 'unexisting_source'
                                  },
                                  context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                                  executor=AsyncioExecutor())
        self.assertIn('errors', response)
        self.assertGreater(len(response['errors']), 0)

    @async_test
    async def test_unfollow_source(self):
        """
        Test unfollowing a source unfollows it
        """
        await self.source_service.save(name=self.TEST_SOURCE)
        await self.user_service.save(id=self.USER_ID, username='test')
        client = Client(schema)
        executor = AsyncioExecutor()
        client.execute(self.FOLLOW_SOURCE_MUTATION,
                       variable_values={
                           'name': self.TEST_SOURCE
                       },
                       context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                       executor=executor)
        with self.session_provider():
            source = await self.source_service.read_one(name=self.TEST_SOURCE)
            self.assertTrue(len(source.follows))
        client.execute(self.UNFOLLOW_SOURCE_MUTATION,
                       variable_values={
                           'name': self.TEST_SOURCE
                       },
                       context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                       executor=executor)
        with self.session_provider():
            source = await self.source_service.read_one(name=self.TEST_SOURCE)
            self.assertFalse(len(source.follows))

    @async_test
    async def test_unfollow_source_not_followed(self):
        """
        Test unfollowing a source not followed returns error
        """
        await self.user_service.save(id=self.USER_ID, username='test')
        client = Client(schema)
        executor = AsyncioExecutor()
        response = client.execute(self.UNFOLLOW_SOURCE_MUTATION,
                                  variables={
                                       'name': self.TEST_SOURCE
                                  },
                                  context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                                  executor=executor)
        self.assertIn('errors', response)
        self.assertGreater(len(response['errors']), 0)
