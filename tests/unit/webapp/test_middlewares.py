"""
Middlewares tests module
"""
from unittest import TestCase
from unittest.mock import Mock

from aiohttp.abc import Request
from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPException
from aiounittest import async_test
from elasticapm import Client

from webapp.container_config import container
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
        container.reset()

        self.apm_mock = Mock(spec=Client)
        container.set('apm', self.apm_mock)
        app = Application()
        self.app = app

    @async_test
    async def test_error_middleware_success(self):
        """
        Test running the error middleware successfully returns the handler response and anf handles the apm transaction
        """
        test_request = Mock(spec=Request)

        async def mock_handler(test):
            """
            Mocked request handler
            """
            return test

        decorated_callable = await error_middleware(self.app, mock_handler)
        decorated_response = await decorated_callable(test_request)
        self.assertEqual(decorated_response, test_request)
        self.apm_mock.begin_transaction.assert_called_once()
        self.apm_mock.end_transaction.assert_called_once()

    @async_test
    async def test_error_middleware_httperror(self):
        """
        Test running the error middleware with an HTTPError raised returns a response with the HTTPError status code
        and handles the apm transaction
        """
        test_reason = 'test_reason'
        test_request = Mock(spec=Request)

        async def mock_handler(_):
            """
            Mocked request handler
            """
            raise HTTPCustomError(reason=test_reason)

        decorated_callable = await error_middleware(self.app, mock_handler)
        decorated_response = await decorated_callable(test_request)
        self.assertEqual(decorated_response.status, HTTPCustomError.status_code)
        self.apm_mock.begin_transaction.assert_called_once()
        self.apm_mock.end_transaction.assert_called_once()

    @async_test
    async def test_error_middleware_non_httperror(self):
        """
        Test running the error middleware with a generic error raised returns a response with the 500 status code
        and handles the apm transaction
        """
        test_reason = 'test_reason'
        test_request = Mock(spec=Request)

        async def mock_handler(_):
            """
            Mocked request handler
            """
            raise ValueError(test_reason)

        decorated_callable = await error_middleware(self.app, mock_handler)
        decorated_response = await decorated_callable(test_request)
        self.assertEqual(decorated_response.status, 500)
        self.apm_mock.begin_transaction.assert_called_once()
        self.apm_mock.end_transaction.assert_called_once()
