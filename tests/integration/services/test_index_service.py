import json
import platform
from dataclasses import asdict
from logging import getLogger
from unittest import TestCase
from unittest.mock import patch, Mock

from aiohttp.web_app import Application
from aiounittest import async_test
from dynaconf.loaders import settings_loader
from elasticapm import Client

from config import config
from infrastructure.repositories.named_entity_repository import NamedEntityRepository
from infrastructure.repositories.named_entity_type_repository import NamedEntityTypeRepository
from infrastructure.repositories.new_repository import NewRepository
from infrastructure.repositories.source_repository import SourceRepository
from models.base import BASE
from news_service_lib.models.language import Language
from news_service_lib.models.named_entity import NamedEntity
from news_service_lib.models.new import New
from news_service_lib.storage.sql.engine_type import SqlEngineType
from news_service_lib.storage.sql.session_provider import SqlSessionProvider
from news_service_lib.storage.sql.utils import create_sql_engine

from services.index_service import IndexService
from tests import TEST_CONFIG_PATH
from webapp.container_config import container
from models.new import New as NewModel

LOGGER = getLogger()

TEST_ENTITY_TYPE_1 = "Test entity type 1"
TEST_ENTITY_TYPE_2 = "Test entity type 2"
TEST_NEW = New(
    title="Test title",
    url="https://test.test",
    content="Test content",
    source="Test source",
    sentiment=3.4,
    date=23452435.0,
    language=Language.ENGLISH.value,
    entities=[
        NamedEntity(text="Test entity 1", type=TEST_ENTITY_TYPE_1),
        NamedEntity(text="Test entity 2", type=TEST_ENTITY_TYPE_1),
    ],
)

TEST_NEW_2 = New(
    title="Test title 2",
    url="https://test2.test",
    content="Test content",
    source="Test source",
    sentiment=4.6,
    date=2323452345.0,
    language=Language.ENGLISH.value,
    entities=[
        NamedEntity(text="Test entity 3", type=TEST_ENTITY_TYPE_1),
        NamedEntity(text="Test entity 4", type=TEST_ENTITY_TYPE_2),
    ],
)


class TestIndexService(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        settings_loader(config, filename=TEST_CONFIG_PATH)

    @patch("services.index_service.Process")
    @patch("services.index_service.ExchangeConsumer")
    def setUp(self, consumer_mock, process_mock) -> None:
        container.reset()

        self.apm_mock = Mock(spec=Client)
        container.set("apm", self.apm_mock)
        self.consumer_mock = consumer_mock
        self.process_mock = process_mock
        self.app = Application()

        test_engine = create_sql_engine(SqlEngineType.SQLITE)

        BASE.metadata.bind = test_engine
        BASE.metadata.create_all()

        self.session_provider = SqlSessionProvider(test_engine)

        logger = getLogger()
        self.source_repo = SourceRepository(self.session_provider, logger)
        self.news_repo = NewRepository(self.session_provider, logger)
        self.named_entity_repo = NamedEntityRepository(self.session_provider, logger)
        self.named_entity_type_repo = NamedEntityTypeRepository(self.session_provider, logger)
        self.index_service = IndexService(logger, test_engine)

    def test_initialize_service(self):
        self.consumer_mock.assert_called_once()
        if platform.system() != "Windows":
            self.process_mock.assert_called_with(target=self.consumer_mock().__call__)
            self.process_mock().start.assert_called_once()

    @async_test
    async def test_index_new(self):
        await self.index_service.index_new(TEST_NEW)

        with self.session_provider(read_only=True):
            indexed_new = await self.news_repo.get_one_filtered(title=TEST_NEW.title)
            self.assertIsInstance(indexed_new, NewModel)
            self.assertEqual(indexed_new.title, TEST_NEW.title)
            self.assertEqual(indexed_new.sentiment, TEST_NEW.sentiment)
            self.assertEqual(indexed_new.source.name, TEST_NEW.source)
            self.assertEqual(len(indexed_new.named_entities), 2)

            named_entity_types = await self.named_entity_type_repo.get_filtered()
            self.assertEqual(len(list(named_entity_types)), 1)

    @async_test
    async def test_index_multiple_news(self):
        await self.index_service.index_new(TEST_NEW)
        await self.index_service.index_new(TEST_NEW_2)

        with self.session_provider(read_only=True):
            indexed_news = await self.news_repo.get_filtered()
            self.assertEqual(len(list(indexed_news)), 2)

            sources = await self.source_repo.get_filtered()
            self.assertEqual(len(list(sources)), 1)

            named_entity_types = list(await self.named_entity_type_repo.get_filtered())
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
        index_new_mock_calls = 0

        async def index_new_mock_async(*_):
            nonlocal index_new_mock_calls
            index_new_mock_calls += 1

        new_msg_1 = json.dumps(asdict(TEST_NEW))
        new_msg_2 = json.dumps(asdict(TEST_NEW_2))

        self.index_service.index_new = index_new_mock_async

        self.index_service.index_message(None, None, None, new_msg_1)
        self.index_service.index_message(None, None, None, new_msg_2)

        self.assertEqual(index_new_mock_calls, 2)
        self.assertEqual(self.apm_mock.begin_transaction.call_count, 2)
        self.assertEqual(self.apm_mock.end_transaction.call_count, 2)

    def test_index_message_fail(self):
        async def index_new_mock_async(*_):
            raise Exception("Test exception")

        self.index_service.index_new = index_new_mock_async

        new_msg_1 = json.dumps(asdict(TEST_NEW))
        self.index_service.index_message(None, None, None, new_msg_1)

        self.assertEqual(self.apm_mock.end_transaction.call_count, 1)
        self.assertEqual(self.apm_mock.capture_exception.call_count, 1)

    @async_test
    async def test_shutdown(self):
        await self.index_service.shutdown()
        self.consumer_mock().shutdown.assert_called_once()
        if platform.system() != "Windows":
            self.process_mock().join.assert_called_once()
