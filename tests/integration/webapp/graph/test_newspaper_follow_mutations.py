"""
Newspaper follow mutations tests module
"""
from unittest import TestCase

from aiohttp.web_app import Application
from aiounittest import async_test
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor
import nest_asyncio

from news_service_lib.storage.sql import create_sql_engine, SqlEngineType, SqlSessionProvider, init_sql_db

from models import BASE
from services.crud.newspaper_service import NewspaperService
from services.crud.user_service import UserService
from webapp.graph import schema

nest_asyncio.apply()


class MockRequest:
    """
    Mocked request used for testing purposes
    """
    def __init__(self, user, app):
        self.user = user
        self.app = app


class TestNewspaperFollowMutations(TestCase):
    """
    Newspaper follow mutations test cases implementation
    """
    USER_ID = 1
    TEST_NEWSPAPER = 'test_newspaper'
    FOLLOW_NEWSPAPER_MUTATION = '''
                mutation FollowNewspaper($name: String!){
                    followNewspaper(newspaperName: $name){
                        ok
                    }
                }
            '''

    UNFOLLOW_NEWSPAPER_MUTATION = '''
                    mutation UnfollowNewspaper($name: String!){
                        unfollowNewspaper(newspaperName: $name){
                            ok
                        }
                    }
                '''

    def setUp(self) -> None:
        """
        Set up the test environment creating the database engine
        """
        test_engine = create_sql_engine(SqlEngineType.SQLITE)
        self.session_provider = SqlSessionProvider(test_engine)
        BASE.query = self.session_provider.query_property
        init_sql_db(BASE, test_engine)

        self.newspaper_service = NewspaperService(session_provider=self.session_provider)
        self.user_service = UserService(session_provider=self.session_provider)

        app = Application()
        app['session_provider'] = self.session_provider
        app['newspaper_service'] = self.newspaper_service
        app['user_service'] = self.user_service
        self.app = app

    @async_test
    async def test_follow_newspaper_success(self):
        """
        Test the follow newspaper mutation stores the follow
        """
        await self.user_service.save(id=2, username='test2')
        await self.user_service.save(id=self.USER_ID, username='test')
        await self.newspaper_service.save(name=self.TEST_NEWSPAPER, user_id=2)
        client = Client(schema)
        client.execute(self.FOLLOW_NEWSPAPER_MUTATION,
                       variable_values={
                         'name': self.TEST_NEWSPAPER
                       },
                       context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                       executor=AsyncioExecutor())
        with self.session_provider():
            newspaper = await self.newspaper_service.read_one(name=self.TEST_NEWSPAPER)
            self.assertTrue(len(newspaper.follows))

    @async_test
    async def test_follow_newspaper_same_user(self):
        """
        Test following a newspaper of the same user which requests the follow returns error
        """
        await self.user_service.save(id=2, username='test2')
        await self.user_service.save(id=self.USER_ID, username='test')
        await self.newspaper_service.save(name=self.TEST_NEWSPAPER, user_id=self.USER_ID)
        client = Client(schema)
        response = client.execute(self.FOLLOW_NEWSPAPER_MUTATION,
                                  variable_values={
                                     'name': self.TEST_NEWSPAPER
                                  },
                                  context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                                  executor=AsyncioExecutor())
        self.assertIn('errors', response)
        self.assertGreater(len(response['errors']), 0)

    @async_test
    async def test_follow_unexisting_newspaper(self):
        """
        Test following an unexisting newspaper returns error
        """
        await self.user_service.save(id=self.USER_ID, username='test')
        client = Client(schema)
        response = client.execute(self.FOLLOW_NEWSPAPER_MUTATION,
                                  variable_values={
                                     'name': 'unexisting_newspaper'
                                  },
                                  context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                                  executor=AsyncioExecutor())
        self.assertIn('errors', response)
        self.assertGreater(len(response['errors']), 0)

    @async_test
    async def test_unfollow_newspaper(self):
        """
        Test unfollowing a newspaper unfollows it
        """
        await self.user_service.save(id=2, username='test2')
        await self.user_service.save(id=self.USER_ID, username='test')
        await self.newspaper_service.save(name=self.TEST_NEWSPAPER, user_id=2)
        client = Client(schema)
        executor = AsyncioExecutor()
        client.execute(self.FOLLOW_NEWSPAPER_MUTATION,
                       variable_values={
                           'name': self.TEST_NEWSPAPER
                       },
                       context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                       executor=executor)
        with self.session_provider():
            newspaper = await self.newspaper_service.read_one(name=self.TEST_NEWSPAPER)
            self.assertTrue(len(newspaper.follows))
        client.execute(self.UNFOLLOW_NEWSPAPER_MUTATION,
                       variable_values={
                           'name': self.TEST_NEWSPAPER
                       },
                       context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                       executor=executor)
        with self.session_provider():
            newspaper = await self.newspaper_service.read_one(name=self.TEST_NEWSPAPER)
            self.assertFalse(len(newspaper.follows))

    @async_test
    async def test_unfollow_not_followed_newspaper(self):
        """
        Test unfollowing a non followed newspaper returns error
        """
        await self.user_service.save(id=2, username='test2')
        await self.user_service.save(id=self.USER_ID, username='test')
        await self.newspaper_service.save(name=self.TEST_NEWSPAPER, user_id=2)
        client = Client(schema)
        executor = AsyncioExecutor()
        response = client.execute(self.UNFOLLOW_NEWSPAPER_MUTATION,
                                  variable_values={
                                       'name': self.TEST_NEWSPAPER
                                  },
                                  context_value={'request': MockRequest({'id': self.USER_ID}, self.app)},
                                  executor=executor)
        self.assertIn('errors', response)
        self.assertGreater(len(response['errors']), 0)
