from decimal import Decimal
from logging import Logger
from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from application.get_news.get_news_query import GetNewsQuery
from domain.new.find_news_criteria import FindNewsCriteria
from domain.new.sort_news_criteria import SortNewsCriteria
from domain.source.source import Source

from domain.new.new import New

from application.get_news.get_news_query_handler import GetNewsQueryHandler
from domain.new.new_repository import NewRepository


class TestGetNewsQueryHandler(TestCase):
    def setUp(self) -> None:
        self.new_repository_mock = Mock(spec=NewRepository)
        self.logger_mock = Mock(spec=Logger)
        self.query_handler = GetNewsQueryHandler(
            self.new_repository_mock,
            self.logger_mock
        )

    def test_handle_success_no_sorting(self):
        test_new = New(
            id=uuid4(),
            title="test_title",
            url="test_url",
            sentiment=Decimal("10.0"),
            source=Source(name="test_source"),
            named_entities=[]
        )
        self.new_repository_mock.find_by_criteria.return_value = [test_new, test_new]
        test_query = GetNewsQuery(
            title="test_new",
            any_named_entity=["test_named_entity_1", "test_named_entity_2"],
            all_named_entities=["test_named_entity_3", "test_named_entity_4"],
            source="test_source",
            sorting=None
        )

        query_response = self.query_handler.handle(test_query)

        self.assertEqual([test_new, test_new], query_response.data)
        self.new_repository_mock.find_by_criteria.assert_called_once_with(FindNewsCriteria(
            title="test_new",
            any_named_entity_value=["test_named_entity_1", "test_named_entity_2"],
            all_named_entities_values=["test_named_entity_3", "test_named_entity_4"],
            source_name="test_source",
        ), None)

    def test_handle_success_sorting(self):
        test_new = New(
            id=uuid4(),
            title="test_title",
            url="test_url",
            sentiment=Decimal("10.0"),
            source=Source(name="test_source"),
            named_entities=[]
        )
        self.new_repository_mock.find_by_criteria.return_value = [test_new, test_new]
        test_query = GetNewsQuery(
            title="test_new",
            any_named_entity=["test_named_entity_1", "test_named_entity_2"],
            all_named_entities=["test_named_entity_3", "test_named_entity_4"],
            source="test_source",
            sorting="SENTIMENT_ASCENDANT"
        )

        query_response = self.query_handler.handle(test_query)

        self.assertEqual([test_new, test_new], query_response.data)
        self.new_repository_mock.find_by_criteria.assert_called_once_with(FindNewsCriteria(
            title="test_new",
            any_named_entity_value=["test_named_entity_1", "test_named_entity_2"],
            all_named_entities_values=["test_named_entity_3", "test_named_entity_4"],
            source_name="test_source",
        ), SortNewsCriteria.SENTIMENT_ASCENDANT)
