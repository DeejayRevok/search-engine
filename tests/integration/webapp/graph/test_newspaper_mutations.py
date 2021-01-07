"""
Newspaper mutations tests module
"""
import nest_asyncio
nest_asyncio.apply()

import asyncio
from unittest import TestCase

from aiohttp.web_app import Application
from aiounittest import async_test
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor

from news_service_lib.storage.sql import create_sql_engine, SqlEngineType, SqlSessionProvider, init_sql_db

from models import BASE
from services.crud.named_entity_service import NamedEntityService
from services.crud.named_entity_type_service import NamedEntityTypeService
from services.crud.newspaper_service import NewspaperService
from services.crud.noun_chunk_service import NounChunkService
from webapp.graph import schema


class MockRequest:
    """
    Mocked request used for testing purposes
    """
    def __init__(self, user, app):
        self.user = user
        self.app = app


class TestNewspaperMutations(TestCase):
    """
    Newspaper mutations test cases implementation
    """
    CREATE_NEWSPAPER_MUTATION = '''
                mutation {
                    createNewspaper(name: "test", namedEntities: ["test_entity_1"], nounChunks: ["test_noun_chunk_1"]){
                        name
                    }
                }
            '''

    UPDATE_NEWSPAPER_MUTATION = '''
                    mutation {
                        updateNewspaper(originalName: "test", updateName: "updateName", namedEntities: ["test_entity_1", 
                                        "test_entity_2"], nounChunks: ["test_noun_chunk_1", "test_noun_chunk_2"]){
                            name
                        }
                    }
                '''

    DELETE_NEWSPAPER_MUTATION = '''
                        mutation {
                            deleteNewspaper(name: "test"){
                                ok
                            }
                        }
                    '''

    TEST_ENTITY_1 = 'test_entity_1'
    TEST_ENTITY_2 = 'test_entity_2'

    TEST_NOUN_CHUNK_1 = 'test_noun_chunk_1'
    TEST_NOUN_CHUNK_2 = 'test_noun_chunk_2'
    TEST_NOUN_CHUNK_3 = 'test_noun_chunk_3'

    def setUp(self) -> None:
        """
        Set up the test environment creating the database engine
        """
        test_engine = create_sql_engine(SqlEngineType.SQLITE)
        self.session_provider = SqlSessionProvider(test_engine)
        BASE.query = self.session_provider.query_property
        init_sql_db(BASE, test_engine)

        named_entity_type_service = NamedEntityTypeService(session_provider=self.session_provider)
        named_entity_service = NamedEntityService(session_provider=self.session_provider)
        named_entity_type = asyncio.run(named_entity_type_service.save(name='TEST'))
        asyncio.run(named_entity_service.save(value=self.TEST_ENTITY_1, named_entity_type_id=named_entity_type.id))
        asyncio.run(named_entity_service.save(value=self.TEST_ENTITY_2, named_entity_type_id=named_entity_type.id))

        noun_chunks_service = NounChunkService(session_provider=self.session_provider)
        asyncio.run(noun_chunks_service.save(value=self.TEST_NOUN_CHUNK_1))
        asyncio.run(noun_chunks_service.save(value=self.TEST_NOUN_CHUNK_2))
        asyncio.run(noun_chunks_service.save(value=self.TEST_NOUN_CHUNK_3))

        self.newspaper_service = NewspaperService(session_provider=self.session_provider)

        app = Application()
        app['session_provider'] = self.session_provider
        app['named_entity_service'] = named_entity_service
        app['noun_chunks_service'] = noun_chunks_service
        app['newspaper_service'] = self.newspaper_service
        self.app = app

    @async_test
    async def test_create_newspaper(self):
        """
        Test the create newspaper mutation creates the newspaper with the input parameters
        """
        client = Client(schema)
        client.execute(self.CREATE_NEWSPAPER_MUTATION,
                       context_value={'request': MockRequest({'id': 1}, self.app)},
                       executor=AsyncioExecutor())
        with self.session_provider():
            created_newspaper = await self.newspaper_service.read_one(name='test')
            self.assertIsNotNone(created_newspaper)
            self.assertEqual(len(created_newspaper.named_entities), 1)
            self.assertEqual(len(created_newspaper.noun_chunks), 1)

    @async_test
    async def test_update_newspaper(self):
        """
        Test the update newspaper mutation updates the previously created newspaper
        """
        client = Client(schema)
        executor = AsyncioExecutor()
        client.execute(self.CREATE_NEWSPAPER_MUTATION,
                       context_value={'request': MockRequest({'id': 1}, self.app)},
                       executor=executor)
        client.execute(self.UPDATE_NEWSPAPER_MUTATION,
                       context_value={'request': MockRequest({'id': 1}, self.app)},
                       executor=executor)
        with self.session_provider():
            created_newspaper = await self.newspaper_service.read_one(name='test')
            self.assertIsNone(created_newspaper)

            updated_newspaper = await self.newspaper_service.read_one(name='updateName')
            self.assertEqual(len(updated_newspaper.named_entities), 2)
            self.assertEqual(len(updated_newspaper.noun_chunks), 2)

    @async_test
    async def test_delete_newspaper(self):
        """
        Test the delete newspaper mutations deletes the previously created newspaper
        """
        client = Client(schema)
        executor = AsyncioExecutor()
        client.execute(self.CREATE_NEWSPAPER_MUTATION,
                       context_value={'request': MockRequest({'id': 1}, self.app)},
                       executor=executor)
        client.execute(self.DELETE_NEWSPAPER_MUTATION,
                       context_value={'request': MockRequest({'id': 1}, self.app)},
                       executor=executor)
        with self.session_provider():
            deleted_newspaper = await self.newspaper_service.read_one(name='test')
            self.assertIsNone(deleted_newspaper)
