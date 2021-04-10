"""
Search engine main tests module
"""
import unittest
from unittest.mock import patch

from aiohttp.web_app import Application
from dynaconf.loaders import settings_loader

from config import config
from tests import TEST_CONFIG_PATH
from webapp.main import init_search_engine


class TestMain(unittest.TestCase):
    """
    Main webapp script test cases implementation
    """

    @patch('webapp.main.container')
    @patch('webapp.main.load')
    @patch('webapp.main.setup_event_bus')
    @patch('webapp.main.setup_graphql_routes')
    @patch('webapp.main.sql_health_check')
    @patch('webapp.main.init_sql_db')
    def test_init_app(self, init_sql_mock, sql_health_mock, setup_graphql_mock, event_bus_mock, load_mock, _):
        """
        Test initializing the app initializes the database the graphql views and all the required services
        """
        settings_loader(config, filename=TEST_CONFIG_PATH)
        sql_health_mock().return_value = True
        base_app = Application()
        init_search_engine(base_app)

        event_bus_mock.assert_called_once()
        load_mock.assert_called_once()

        init_sql_mock.assert_called_once()
        setup_graphql_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
