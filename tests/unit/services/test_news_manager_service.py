from logging import getLogger
from unittest import TestCase

from gql import gql
from unittest.mock import patch

from aiounittest import async_test

from services.news_manager_service import NewsManagerService


class TestNewsManagerService(TestCase):

    GET_NEW_BY_TITLE_QUERY = gql(
        """
        query getNewByTitle($searchTitle: String!) {
            new(title: $searchTitle){
                title
                url
                content
                source
                date
                hydrated
                entities {
                  text
                  type
                }
                summary
                sentiment
                nounChunks
            }
        }
    """
    )

    @patch("services.news_manager_service.RequestsHTTPTransport")
    @patch("services.news_manager_service.encode")
    @patch("services.news_manager_service.Client")
    @async_test
    async def test_get_new_title(self, mock_gql_client, encode_mock, _):
        encode_mock.return_value = b"test_token_encoded"
        news_manager_service = NewsManagerService("test", "test", "test", "test", getLogger())

        test_title = "Test title"
        await news_manager_service.get_new_by_title(test_title)
        mock_gql_client().execute.assert_called_with(
            self.GET_NEW_BY_TITLE_QUERY, variable_values=dict(searchTitle=test_title)
        )
