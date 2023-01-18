from logging import Logger

from bus_station.command_terminal.command_handler import CommandHandler

from application.save_user.save_user_command import SaveUserCommand
from domain.user.user import User
from domain.user.user_repository import UserRepository


class SaveUserCommandHandler(CommandHandler):
    def __init__(self, user_repository: UserRepository, logger: Logger):
        self.__user_repository = user_repository
        self.__logger = logger

    def handle(self, command: SaveUserCommand) -> None:
        self.__logger.info(f"Starting saving user {command.email}")

        user = User(email=command.email)
        self.__user_repository.save(user)

        self.__logger.info(f"Finished saving user {command.email}")

    @classmethod
    def bus_stop_name(cls) -> str:
        return "command_handler.search_engine.save_user"
