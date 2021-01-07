"""
Middlewares tests module
"""
from unittest import TestCase
from unittest.mock import MagicMock

from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPException
from aiounittest import async_test

from webapp.middlewares import error_middleware


class HTTPCustomError(HTTPException):
    """
    Custom HTTP Error implementation
    """
    status_code = 1234


class TestMiddlewares(TestCase):
    """
    Middlewares test cases implementation
    """
    def setUp(self) -> None:
        """
        Set up the test environment
        """
        self.apm_mock_client = MagicMock()
        apm_mock = MagicMock()
        apm_mock.client = self.apm_mock_client
        app = Application()
        app['apm'] = apm_mock
        self.app = app

    @async_test
    async def test_error_middleware_success(self):
        """
        Test running the error middleware successfully returns the handler response and anf handles the apm transaction
        """
        test_request = MagicMock()

        async def mock_handler(test):
            """
            Mocked request handler
            """
            return test

        decorated_callable = await error_middleware(self.app, mock_handler)
        decorated_response = await decorated_callable(test_request)
        self.assertEqual(decorated_response, test_request)
        self.apm_mock_client.begin_transaction.assert_called_once()
        self.apm_mock_client.end_transaction.assert_called_once()

    @async_test
    async def test_error_middleware_httperror(self):
        """
        Test running the error middleware with an HTTPError raised returns a response with the HTTPError status code
        and handles the apm transaction
        """
        test_reason = 'test_reason'
        test_request = MagicMock()

        async def mock_handler(_):
            """
            Mocked request handler
            """
            raise HTTPCustomError(reason=test_reason)

        decorated_callable = await error_middleware(self.app, mock_handler)
        decorated_response = await decorated_callable(test_request)
        self.assertEqual(decorated_response.status, HTTPCustomError.status_code)
        self.apm_mock_client.begin_transaction.assert_called_once()
        self.apm_mock_client.end_transaction.assert_called_once()

    @async_test
    async def test_error_middleware_non_httperror(self):
        """
        Test running the error middleware with a generic error raised returns a response with the 500 status code
        and handles the apm transaction
        """
        test_reason = 'test_reason'
        test_request = MagicMock()

        async def mock_handler(_):
            """
            Mocked request handler
            """
            raise ValueError(test_reason)

        decorated_callable = await error_middleware(self.app, mock_handler)
        decorated_response = await decorated_callable(test_request)
        self.assertEqual(decorated_response.status, 500)
        self.apm_mock_client.begin_transaction.assert_called_once()
        self.apm_mock_client.end_transaction.assert_called_once()
