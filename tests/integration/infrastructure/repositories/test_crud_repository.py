from logging import getLogger
from unittest import TestCase

from aiounittest import async_test
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from infrastructure.repositories.crud_repository import CRUDRepository
from news_service_lib.storage.sql.engine_type import SqlEngineType
from news_service_lib.storage.sql.session_provider import SqlSessionProvider
from news_service_lib.storage.sql.utils import create_sql_engine

LOGGER = getLogger()
BASE = declarative_base()


class TestModel(BASE):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    test1 = Column(String(50))
    test2 = Column(String(50))


class TestCRUDRepository(TestCase):
    TEST_1 = "test_1"
    TEST_2 = "test_2"

    def setUp(self):
        test_engine = create_sql_engine(SqlEngineType.SQLITE)
        BASE.metadata.bind = test_engine
        BASE.metadata.create_all()
        session_provider = SqlSessionProvider(test_engine)
        self.repository = CRUDRepository(session_provider, LOGGER)
        self.repository._ENTITY_CLASS = TestModel

    @async_test
    async def test_save(self):
        await self.repository.save(TestModel(test1=self.TEST_1, test2=self.TEST_2))
        model_instances = list(await self.repository.get_filtered())
        self.assertIsNotNone(model_instances)
        self.assertEqual(len(model_instances), 1)
        self.assertEqual(model_instances[0].test1, self.TEST_1)
        self.assertEqual(model_instances[0].test2, self.TEST_2)

    @async_test
    async def test_get_filtered_all(self):
        await self.repository.save(TestModel(test1="test_11", test2="test_12"))
        await self.repository.save(TestModel(test1="test_21", test2="test_22"))
        model_instances = list(await self.repository.get_filtered())
        self.assertIsNotNone(model_instances)
        self.assertEqual(len(model_instances), 2)

    @async_test
    async def test_get_one_filtered(self):
        await self.repository.save(TestModel(test1=self.TEST_1, test2=self.TEST_2))
        await self.repository.save(TestModel(test1="test_21", test2="test_22"))
        model_instance = await self.repository.get_one_filtered(test1=self.TEST_1)
        self.assertIsNotNone(model_instance)
        self.assertEqual(model_instance.test1, self.TEST_1)
        self.assertEqual(model_instance.test2, self.TEST_2)

    @async_test
    async def test_delete_existing(self):
        await self.repository.save(TestModel(test1=self.TEST_1, test2=self.TEST_2))
        model_instance = await self.repository.get_one_filtered()
        self.assertIsNotNone(model_instance)

        await self.repository.delete(model_instance)
        model_instance = await self.repository.get_one_filtered()
        self.assertIsNone(model_instance)
