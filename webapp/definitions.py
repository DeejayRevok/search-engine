"""
UAA webapp definitions module
"""
from os.path import join, dirname

from news_service_lib.storage.sql import sql_health_check
from webapp.container_config import container

API_VERSION = 'v1'
ALEMBIC_INI_PATH = join(dirname(dirname(__file__, )), 'alembic.ini')


async def health_check() -> bool:
    """
    Check the health status of the application

    Returns: True if the status is OK, False otherwise

    """
    return sql_health_check(container.get('storage_engine'))
