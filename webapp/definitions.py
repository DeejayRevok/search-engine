"""
UAA webapp definitions module
"""
from os.path import join, dirname

from aiohttp.web_app import Application
from news_service_lib.storage.sql import sql_health_check

API_VERSION = 'v1'
CONFIG_PATH = join(dirname(dirname(__file__, )), 'configs')


async def health_check(app: Application) -> bool:
    """
    Check the health status of the application

    Args:
        app: application to check health

    Returns: True if the status is OK, False otherwise

    """
    return sql_health_check(app['storage_engine'])
