from logging import Logger

from infrastructure.repositories.user_repository import UserRepository
from news_service_lib.events.event_listener import EventListener


class UserDeletedListener(EventListener):
    def __init__(self, name: str, event_api: str, event_name: str, user_repository: UserRepository, logger: Logger):
        super().__init__(name, event_api, event_name)
        self.__user_repository = user_repository
        self.__logger = logger

    async def listener_handler(self, _, uaa_id: int = None):
        self.__logger.info(f"Received user deletion event")
        try:
            user = await self.__user_repository.get_one_filtered(id=uaa_id)
            await self.__user_repository.delete(user)
        except Exception as ex:
            self.__logger.error(f'Error while deleting the view of the created user {ex}', exc_info=True)
