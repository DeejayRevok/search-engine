"""
Search engine main tests module
"""
import unittest
from unittest.mock import patch

from aiohttp.web_app import Application
from news_service_lib.config import Configuration
from webapp.main import init_search_engine


class TestMain(unittest.TestCase):
    """
    Main webapp script test cases implementation
    """

    # noinspection PyTypeHints
    @patch('webapp.main.get_uaa_service')
    @patch('webapp.main.NewsManagerService')
    @patch('webapp.main.IndexService')
    @patch('webapp.main.setup_graphql_routes')
    @patch.object(Configuration, 'get')
    @patch('webapp.main.initialize_apm')
    @patch('webapp.main.SqlSessionProvider')
    @patch('webapp.main.sql_health_check')
    @patch('webapp.main.init_sql_db')
    @patch('webapp.main.create_sql_engine')
    def test_init_app(self, create_engine_mock, init_sql_mock, sql_health_mock, _,
                      initialize_apm_mock, config_mock, setup_graphql_mock, index_service_mock, news_manager_mock,
                      get_uaa_service_mock):
        """
        Test initializing the app initializes the database the graphql views and all the required services
        """
        sql_health_mock().return_value = True
        base_app = Application()
        base_app['config'] = config_mock
        app = init_search_engine(base_app)

        self.assertIsNotNone(app['session_provider'])
        self.assertIsNotNone(app['source_service'])
        self.assertIsNotNone(app['new_service'])
        self.assertIsNotNone(app['named_entity_service'])
        self.assertIsNotNone(app['named_entity_type_service'])
        self.assertIsNotNone(app['index_service'])
        self.assertIsNotNone(app['news_manager_service'])
        self.assertIsNotNone(app['uaa_service'])

        create_engine_mock.assert_called_once()
        init_sql_mock.assert_called_once()
        initialize_apm_mock.assert_called_once()
        setup_graphql_mock.assert_called_once()

        index_service_mock.assert_called_once()
        news_manager_mock.assert_called_once()
        get_uaa_service_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
