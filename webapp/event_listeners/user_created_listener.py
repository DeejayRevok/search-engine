"""
User created listener definition module
"""
from log_config import get_logger
from news_service_lib.events.event_listener import EventListener
from news_service_lib.storage.sql import SqlSessionProvider, create_sql_engine, SqlEngineType
from services.crud.user_service import UserService

LOGGER = get_logger()


class UserCreatedListener(EventListener):
    """
    User created listener implementation
    """
    def __init__(self, name: str, event_api: str, event_name: str, storage_config: dict):
        super().__init__(name, event_api, event_name)
        storage_engine = create_sql_engine(SqlEngineType.MYSQL, **storage_config)
        self.session_provider = SqlSessionProvider(storage_engine)
        self.user_service = UserService(self.session_provider)

    async def listener_handler(self, _, uaa_id: int = None, username: str = None):
        LOGGER.info(f"Received user creation event of {username}")
        try:
            with self.session_provider(read_only=False):
                await self.user_service.save(id=uaa_id, username=username)
        except Exception as ex:
            LOGGER.error(f'Error while saving the view of the created user {ex}', exc_info=True)
