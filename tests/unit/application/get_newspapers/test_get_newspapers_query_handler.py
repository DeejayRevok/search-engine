from logging import Logger
from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from application.get_newspapers.get_newspapers_query import GetNewspapersQuery
from application.get_newspapers.get_newspapers_query_handler import GetNewspapersQueryHandler
from domain.newspaper.find_newspaper_criteria import FindNewspaperCriteria
from domain.newspaper.newspaper import Newspaper
from domain.newspaper.newspaper_repository import NewspaperRepository


class TestGetNewspapersQueryHandler(TestCase):
    def setUp(self) -> None:
        self.newspaper_repository_mock = Mock(spec=NewspaperRepository)
        self.logger_mock = Mock(spec=Logger)
        self.query_handler = GetNewspapersQueryHandler(
            self.newspaper_repository_mock,
            self.logger_mock
        )

    def test_handle_success(self):
        test_newspaper = Newspaper(
            id=uuid4(),
            name="test_newspaper",
            user_email="test_user",
            named_entities=[]
        )
        self.newspaper_repository_mock.find_by_criteria.return_value = [test_newspaper, test_newspaper]
        test_query = GetNewspapersQuery(
            user_email="test_user"
        )

        query_response = self.query_handler.handle(test_query)

        self.assertEqual([test_newspaper, test_newspaper], query_response.data)
        self.newspaper_repository_mock.find_by_criteria.assert_called_once_with(FindNewspaperCriteria(
            user_email="test_user"
        ))
