"""
Index service tests module
"""
import json
from logging import getLogger
from unittest import TestCase
from unittest.mock import patch, MagicMock

from aiohttp.web_app import Application
from aiounittest import async_test

from models import BASE, New as NewModel
from news_service_lib.models import New, NamedEntity
from news_service_lib.storage.sql import create_sql_engine, SqlEngineType, init_sql_db, SqlSessionProvider
from services.crud.named_entity_service import NamedEntityService
from services.crud.named_entity_type_service import NamedEntityTypeService
from services.crud.new_service import NewService
from services.crud.source_service import SourceService
from services.index_service import IndexService

LOGGER = getLogger()

TEST_ENTITY_TYPE_1 = "Test entity type 1"
TEST_ENTITY_TYPE_2 = "Test entity type 2"
TEST_NEW = New(title="Test title",
               content="Test content",
               source="Test source",
               sentiment=3.4,
               date=23452435.0,
               entities=[NamedEntity(text="Test entity 1", type=TEST_ENTITY_TYPE_1),
                         NamedEntity(text="Test entity 2", type=TEST_ENTITY_TYPE_1)])

TEST_NEW_2 = New(title="Test title 2",
                 content="Test content",
                 source="Test source",
                 sentiment=4.6,
                 date=2323452345.0,
                 entities=[NamedEntity(text="Test entity 3", type=TEST_ENTITY_TYPE_1),
                           NamedEntity(text="Test entity 4", type=TEST_ENTITY_TYPE_2)])


class TestIndexService(TestCase):
    """
    Index service test cases implementation
    """

    @patch('services.index_service.Process')
    @patch('services.index_service.ExchangeConsumer')
    def setUp(self, consumer_mock, process_mock) -> None:
        self.consumer_mock = consumer_mock
        self.process_mock = process_mock
        self.app = Application()
        self.app['config'] = MagicMock()

        self.apm_mock = MagicMock()
        self.app['apm'] = MagicMock()
        self.app['apm'].client = self.apm_mock

        test_engine = create_sql_engine(SqlEngineType.SQLITE)
        init_sql_db(BASE, test_engine)
        self.session_provider = SqlSessionProvider(test_engine)

        self.source_service = SourceService(self.session_provider)
        self.news_service = NewService(self.session_provider)
        self.named_entity_service = NamedEntityService(self.session_provider)
        self.named_entity_type_service = NamedEntityTypeService(self.session_provider)
        self.app['source_service'] = self.source_service
        self.app['new_service'] = self.news_service
        self.app['named_entity_service'] = self.named_entity_service
        self.app['named_entity_type_service'] = self.named_entity_type_service
        self.app['session_provider'] = self.session_provider
        self.index_service = IndexService(self.app)

    def test_initialize_service(self):
        """
        Test initializing the index service initializes the associated exchange consumer in separated process
        and starts the process
        """
        self.consumer_mock.assert_called_once()
        self.process_mock.assert_called_with(target=self.consumer_mock().__call__)
        self.process_mock().start.assert_called_once()

    @async_test
    async def test_index_new(self):
        """
        Test the indexing a new creates the new entity the source entity and its associated named entities
        and named entity types
        """
        await self.index_service.index_new(TEST_NEW)

        with self.session_provider(read_only=True):
            indexed_new = await self.news_service.read_one(title=TEST_NEW.title)
            self.assertIsInstance(indexed_new, NewModel)
            self.assertEqual(indexed_new.title, TEST_NEW.title)
            self.assertEqual(indexed_new.sentiment, TEST_NEW.sentiment)
            self.assertEqual(indexed_new.source.name, TEST_NEW.source)
            self.assertEqual(len(indexed_new.named_entities), 2)

            named_entity_types = await self.named_entity_type_service.read_all()
            self.assertEqual(len(list(named_entity_types)), 1)

    @async_test
    async def test_index_multiple_news(self):
        """
        Test the indexing multiple news creates the new entities the source entities and its associated named entities
        and named entity types
        """
        await self.index_service.index_new(TEST_NEW)
        await self.index_service.index_new(TEST_NEW_2)

        with self.session_provider(read_only=True):
            indexed_news = await self.news_service.read_all()
            self.assertEqual(len(list(indexed_news)), 2)

            sources = await self.source_service.read_all()
            self.assertEqual(len(list(sources)), 1)

            named_entity_types = list(await self.named_entity_type_service.read_all())
            self.assertEqual(len(named_entity_types), 2)

            named_entity_type_1 = next(filter(lambda net: net.name == TEST_ENTITY_TYPE_1, named_entity_types))
            self.assertIsNotNone(named_entity_type_1)

            named_entity_type_2 = next(filter(lambda net: net.name == TEST_ENTITY_TYPE_2, named_entity_types))
            self.assertIsNotNone(named_entity_type_2)

            named_entities_type_1 = named_entity_type_1.named_entities
            self.assertEqual(len(named_entities_type_1), 3)

            named_entities_type_2 = named_entity_type_2.named_entities
            self.assertEqual(len(named_entities_type_2), 1)

    def test_index_message(self):
        """
        Test indexing multiple messages calls the index message and manages the transaction
        """
        index_new_mock_calls = 0

        async def index_new_mock_async(*_):
            nonlocal index_new_mock_calls
            index_new_mock_calls += 1

        new_msg_1 = json.dumps(dict(TEST_NEW))
        new_msg_2 = json.dumps(dict(TEST_NEW_2))

        self.index_service.index_new = index_new_mock_async

        self.index_service.index_message(None, None, None, new_msg_1)
        self.index_service.index_message(None, None, None, new_msg_2)

        self.assertEqual(index_new_mock_calls, 2)
        self.assertEqual(self.apm_mock.begin_transaction.call_count, 2)
        self.assertEqual(self.apm_mock.end_transaction.call_count, 2)

    def test_index_message_fail(self):
        """
        Test if index new fails the apm client ends the transaction and captures the exception
        """
        async def index_new_mock_async(*_):
            raise Exception('Test exception')

        self.index_service.index_new = index_new_mock_async

        new_msg_1 = json.dumps(dict(TEST_NEW))
        self.index_service.index_message(None, None, None, new_msg_1)

        self.assertEqual(self.apm_mock.end_transaction.call_count, 1)
        self.assertEqual(self.apm_mock.capture_exception.call_count, 1)

    @async_test
    async def test_shutdown(self):
        """
        Test shutting down the service shuts down the consumer and wait the consumer process to join
        """
        await self.index_service.shutdown()
        self.consumer_mock().shutdown.assert_called_once()
        self.process_mock().join.assert_called_once()
