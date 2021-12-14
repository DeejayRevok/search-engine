from unittest import TestCase
from unittest.mock import MagicMock, Mock

from aiohttp.abc import Request
from aiohttp.web_exceptions import HTTPUnauthorized
from graphql import ResolveInfo

from webapp.graph.utils.authenticated_filterable_field import AuthenticatedFilterableField


class TestGraphUtils(TestCase):
    def test_authenticated_field_success(self):
        mock_request = Mock(spec=Request)
        mock_request.user = 'test'
        mock_resolve_info = Mock(spec=ResolveInfo)
        mock_resolve_info.context = {'request': mock_request}
        mock_connection = MagicMock(name='test')
        result_connection = AuthenticatedFilterableField.resolve_connection(mock_connection, MagicMock(),
                                                                            mock_resolve_info, MagicMock(),
                                                                            MagicMock())
        self.assertEqual(result_connection, mock_connection())

    def test_authenticated_field_fails(self):
        mock_request = Mock(spec=Request)
        mock_request.user = None
        mock_resolve_info = Mock(spec=ResolveInfo)
        mock_resolve_info.context = {'request': mock_request}
        mock_connection = MagicMock(name='test')
        with self.assertRaises(HTTPUnauthorized):
            AuthenticatedFilterableField.resolve_connection(mock_connection, MagicMock(),
                                                            mock_resolve_info, MagicMock(),
                                                            MagicMock())
