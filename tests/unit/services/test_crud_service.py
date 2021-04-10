"""
CRUD service tests module
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock

from aiounittest import async_test
from news_service_lib.storage import StorageError
from news_service_lib.storage.implementation import Storage
from services.crud.crud_service import CRUDService


class TestCRUDService(TestCase):
    """
    CRUD service test cases implementation
    """
    @patch('services.crud.crud_service.storage_factory')
    def setUp(self, factory_mock) -> None:
        self.test_entity_instance = MagicMock()
        self.test_entity = MagicMock()
        self.test_entity.return_value = self.test_entity_instance
        CRUDService.entity_class = self.test_entity
        self._repo_mock = Mock(spec=Storage)
        factory_mock.return_value = self._repo_mock
        self.test_crud_service = CRUDService(MagicMock())

    @async_test
    async def test_save(self):
        """
        Test saving creates an instance of the CRUD service entity class and calls the repo to save the
        created instance
        """
        test_value = 'TEST'
        await self.test_crud_service.save(test=test_value)
        self.test_entity.assert_called_with(test=test_value)
        self._repo_mock.save.assert_called_with(self.test_entity_instance)

    @async_test
    async def test_save_storage_error(self):
        """
        Test storage error when saving raises a value error
        """
        self._repo_mock.save.side_effect = MagicMock(side_effect=StorageError('Test'))
        test_value = 'TEST'
        with self.assertRaises(ValueError):
            await self.test_crud_service.save(test=test_value)

    @async_test
    async def test_update(self):
        """
        Test updating an existing entity instance sets its property to the updated value and
        saves the updated entity
        """
        test_value = 'TEST'
        entity_instance_mock = MagicMock(spec=['test'])
        await self.test_crud_service.update(entity_instance_mock, test=test_value)
        self.assertEqual(entity_instance_mock.test, test_value)
        self._repo_mock.save.assert_called_with(entity_instance_mock)

    @async_test
    async def test_update_wrong_property(self):
        """
        Test trying to update a non existing property of an entity fails
        """
        test_value = 'TEST'
        entity_instance_mock = MagicMock(spec=['test'])
        with self.assertRaises(ValueError):
            await self.test_crud_service.update(entity_instance_mock, test_wrong=test_value)

    @async_test
    async def test_update_storage_error(self):
        """
        Test storage error when updating raises a value error
        """
        self._repo_mock.save.side_effect = MagicMock(side_effect=StorageError('Test'))
        test_value = 'TEST'
        entity_instance_mock = MagicMock(spec=['test'])
        with self.assertRaises(ValueError):
            await self.test_crud_service.update(entity_instance_mock, test=test_value)

    @async_test
    async def test_delete(self):
        """
        Test deleting calls the repo delete with the provided identifier
        """
        test_value = 'TEST'
        await self.test_crud_service.delete(test_value)
        self._repo_mock.delete.assert_called_with(test_value)

    @async_test
    async def test_read_all(self):
        """
        Test read all with filters calls the repo get with the parsed filters
        """
        test1_value = 'TEST1'
        test2_value = 'TEST2'
        await self.test_crud_service.read_all(test1=test1_value, test2=test2_value)
        self._repo_mock.get.assert_called_once()
        get_call_args = self._repo_mock.get.call_args[0][0]
        self.assertEqual(len(get_call_args), 2)
        self.assertEqual(get_call_args[0].key, 'test1')
        self.assertEqual(get_call_args[0].value, test1_value)
        self.assertEqual(get_call_args[1].key, 'test2')
        self.assertEqual(get_call_args[1].value, test2_value)

    @async_test
    async def test_read_one(self):
        """
        Test read one with filters calls the repo get with the parsed filters
        """
        test1_value = 'TEST1'
        test2_value = 'TEST2'
        await self.test_crud_service.read_one(test1=test1_value, test2=test2_value)
        self._repo_mock.get_one.assert_called_once()
        get_call_args = self._repo_mock.get_one.call_args[0][0]
        self.assertEqual(len(get_call_args), 2)
        self.assertEqual(get_call_args[0].key, 'test1')
        self.assertEqual(get_call_args[0].value, test1_value)
        self.assertEqual(get_call_args[1].key, 'test2')
        self.assertEqual(get_call_args[1].value, test2_value)

