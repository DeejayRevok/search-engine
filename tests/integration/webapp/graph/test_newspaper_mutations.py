from logging import getLogger
from unittest import TestCase

import asyncio
from aiohttp.web_app import Application
from aiounittest import async_test
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor
import nest_asyncio

from infrastructure.repositories.named_entity_repository import NamedEntityRepository
from infrastructure.repositories.named_entity_type_repository import NamedEntityTypeRepository
from infrastructure.repositories.newspaper_repository import NewspaperRepository
from infrastructure.repositories.noun_chunk_repository import NounChunkRepository
from models.base import BASE

from models.named_entity import NamedEntity
from models.named_entity_type import NamedEntityType
from models.noun_chunk import NounChunk
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


class TestNewspaperMutations(TestCase):
    CREATE_NEWSPAPER_MUTATION = """
                mutation {
                    createNewspaper(name: "test", namedEntities: ["test_entity_1"], nounChunks: ["test_noun_chunk_1"]){
                        name
                    }
                }
            """

    UPDATE_NEWSPAPER_MUTATION = """
                    mutation {
                        updateNewspaper(originalName: "test", updateName: "updateName", namedEntities: ["test_entity_1", 
                                        "test_entity_2"], nounChunks: ["test_noun_chunk_1", "test_noun_chunk_2"]){
                            name
                        }
                    }
                """

    DELETE_NEWSPAPER_MUTATION = """
                        mutation {
                            deleteNewspaper(name: "test"){
                                ok
                            }
                        }
                    """

    TEST_ENTITY_1 = "test_entity_1"
    TEST_ENTITY_2 = "test_entity_2"

    TEST_NOUN_CHUNK_1 = "test_noun_chunk_1"
    TEST_NOUN_CHUNK_2 = "test_noun_chunk_2"
    TEST_NOUN_CHUNK_3 = "test_noun_chunk_3"

    def setUp(self) -> None:
        container.reset()
        test_engine = create_sql_engine(SqlEngineType.SQLITE)
        self.session_provider = SqlSessionProvider(test_engine)
        BASE.query = self.session_provider.query_property
        BASE.metadata.bind = test_engine
        BASE.metadata.create_all()
        logger = getLogger()

        named_entity_type_repository = NamedEntityTypeRepository(self.session_provider, logger)
        named_entity_repository = NamedEntityRepository(self.session_provider, logger)
        named_entity_type = asyncio.run(named_entity_type_repository.save(NamedEntityType(name="TEST")))
        asyncio.run(
            named_entity_repository.save(
                NamedEntity(value=self.TEST_ENTITY_1, named_entity_type_id=named_entity_type.id)
            )
        )
        asyncio.run(
            named_entity_repository.save(
                NamedEntity(value=self.TEST_ENTITY_2, named_entity_type_id=named_entity_type.id)
            )
        )

        noun_chunks_repository = NounChunkRepository(self.session_provider, logger)
        asyncio.run(noun_chunks_repository.save(NounChunk(value=self.TEST_NOUN_CHUNK_1)))
        asyncio.run(noun_chunks_repository.save(NounChunk(value=self.TEST_NOUN_CHUNK_2)))
        asyncio.run(noun_chunks_repository.save(NounChunk(value=self.TEST_NOUN_CHUNK_3)))

        self.newspaper_repository = NewspaperRepository(self.session_provider, logger)

        app = Application()
        container.set("session_provider", self.session_provider)
        container.set("named_entity_repository", named_entity_repository)
        container.set("noun_chunk_repository", noun_chunks_repository)
        container.set("newspaper_repository", self.newspaper_repository)
        self.app = app

    @async_test
    async def test_create_newspaper(self):
        client = Client(schema)
        client.execute(
            self.CREATE_NEWSPAPER_MUTATION,
            context_value={"request": MockRequest({"id": 1}, self.app)},
            executor=AsyncioExecutor(),
        )
        with self.session_provider():
            created_newspaper = await self.newspaper_repository.get_one_filtered(name="test")
            self.assertIsNotNone(created_newspaper)
            self.assertEqual(len(created_newspaper.named_entities), 1)
            self.assertEqual(len(created_newspaper.noun_chunks), 1)

    @async_test
    async def test_update_newspaper(self):
        client = Client(schema)
        executor = AsyncioExecutor()
        client.execute(
            self.CREATE_NEWSPAPER_MUTATION,
            context_value={"request": MockRequest({"id": 1}, self.app)},
            executor=executor,
        )
        client.execute(
            self.UPDATE_NEWSPAPER_MUTATION,
            context_value={"request": MockRequest({"id": 1}, self.app)},
            executor=executor,
        )
        with self.session_provider():
            created_newspaper = await self.newspaper_repository.get_one_filtered(name="test")
            self.assertIsNone(created_newspaper)

            updated_newspaper = await self.newspaper_repository.get_one_filtered(name="updateName")
            self.assertEqual(len(updated_newspaper.named_entities), 2)
            self.assertEqual(len(updated_newspaper.noun_chunks), 2)

    @async_test
    async def test_delete_newspaper(self):
        client = Client(schema)
        executor = AsyncioExecutor()
        client.execute(
            self.CREATE_NEWSPAPER_MUTATION,
            context_value={"request": MockRequest({"id": 1}, self.app)},
            executor=executor,
        )
        client.execute(
            self.DELETE_NEWSPAPER_MUTATION,
            context_value={"request": MockRequest({"id": 1}, self.app)},
            executor=executor,
        )
        with self.session_provider():
            deleted_newspaper = await self.newspaper_repository.get_one_filtered(name="test")
            self.assertIsNone(deleted_newspaper)
