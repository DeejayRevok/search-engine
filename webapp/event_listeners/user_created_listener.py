from logging import Logger

from infrastructure.repositories.user_repository import UserRepository
from models.user import User
from news_service_lib.events.event_listener import EventListener


class UserCreatedListener(EventListener):
    def __init__(self, name: str, event_api: str, event_name: str, user_repository: UserRepository, logger: Logger):
        super().__init__(name, event_api, event_name)
        self.__user_repository = user_repository
        self.__logger = logger

    async def listener_handler(self, _, uaa_id: int = None, username: str = None):
        self.__logger.info(f"Received user creation event of {username}")
        try:
            await self.__user_repository.save(User(id=uaa_id, username=username))
        except Exception as ex:
            self.__logger.error(f'Error while saving the view of the created user {ex}', exc_info=True)
