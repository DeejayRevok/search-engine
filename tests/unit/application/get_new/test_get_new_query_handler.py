from decimal import Decimal
from logging import Logger
from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from application.get_new.get_new_query import GetNewQuery
from domain.source.source import Source
from domain.new.new import New
from application.get_new.get_new_query_handler import GetNewQueryHandler
from domain.new.new_repository import NewRepository


class TestGetNewQueryHandler(TestCase):
    def setUp(self) -> None:
        self.new_repository_mock = Mock(spec=NewRepository)
        self.logger_mock = Mock(spec=Logger)
        self.query_handler = GetNewQueryHandler(
            self.new_repository_mock,
            self.logger_mock
        )

    def test_handle_success(self):
        test_uuid = uuid4()
        test_new = New(
            id=test_uuid,
            title="test_title",
            url="test_url",
            sentiment=Decimal("10.0"),
            source=Source(name="test_source"),
            named_entities=[]
        )
        self.new_repository_mock.find_by_id.return_value = test_new
        test_query = GetNewQuery(id=str(test_uuid))

        query_response = self.query_handler.handle(test_query)

        self.assertEqual(test_new, query_response.data)
        self.new_repository_mock.find_by_id.assert_called_once_with(test_uuid)
