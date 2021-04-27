"""
News manager service testing module
"""
from unittest import TestCase
from unittest.mock import patch

from aiounittest import async_test

from services.news_manager_service import NewsManagerService, GET_NEW_BY_TITLE_QUERY


class TestNewsManagerService(TestCase):
    """
    News manager service test cases implementation
    """
    @patch('services.news_manager_service.get_system_auth_token')
    @patch('services.news_manager_service.RequestsHTTPTransport')
    @patch('services.news_manager_service.Client')
    @async_test
    async def test_get_new_title(self, mock_gql_client, _, __):
        """
        Test calling the get new by title executes the get new by title graphql query with the provided title
        """
        news_manager_service = NewsManagerService('test', 'test', 'test')

        test_title = 'Test title'
        await news_manager_service.get_new_by_title(test_title)
        mock_gql_client().execute.assert_called_with(GET_NEW_BY_TITLE_QUERY,
                                                     variable_values=dict(searchTitle=test_title))
