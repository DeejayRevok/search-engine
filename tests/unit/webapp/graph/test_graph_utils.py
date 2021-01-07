"""
GraphQL utils tests module
"""
from unittest import TestCase
from unittest.mock import MagicMock

from aiohttp.web_exceptions import HTTPUnauthorized

from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class HelperClass:
    """
    Tests helper class
    """
    def __init__(self):
        self.context = None
        self.user = None


class TestGraphUtils(TestCase):
    """
    GraphQL utils test cases implementation
    """
    def test_authenticated_field_success(self):
        """
        Test resolving fields with authenticated requests resolves the field connection
        """
        mock_request = HelperClass()
        mock_request.user = 'test'
        mock_resolve_info = HelperClass()
        mock_resolve_info.context = {'request': mock_request}
        mock_connection = MagicMock(name='test')
        result_connection = AuthenticatedFilterableField.resolve_connection(mock_connection, MagicMock(),
                                                                            mock_resolve_info, MagicMock(),
                                                                            MagicMock())
        self.assertEqual(result_connection, mock_connection())

    def test_authenticated_field_fails(self):
        """
        Test resolving fields without authenticated request raises HTTPUnauthorized error
        """
        mock_request = HelperClass()
        mock_resolve_info = HelperClass()
        mock_resolve_info.context = {'request': mock_request}
        mock_connection = MagicMock(name='test')
        with self.assertRaises(HTTPUnauthorized):
            AuthenticatedFilterableField.resolve_connection(mock_connection, MagicMock(),
                                                            mock_resolve_info, MagicMock(),
                                                            MagicMock())
