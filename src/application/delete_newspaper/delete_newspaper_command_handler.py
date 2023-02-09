from logging import Logger
from uuid import UUID

from bus_station.command_terminal.command_handler import CommandHandler

from application.delete_newspaper.delete_newspaper_command import DeleteNewspaperCommand
from domain.newspaper.newspaper_repository import NewspaperRepository


class DeleteNewspaperCommandHandler(CommandHandler):
    def __init__(self, newspaper_repository: NewspaperRepository, logger: Logger):
        self.__newspaper_repository = newspaper_repository
        self.__logger = logger

    def handle(self, command: DeleteNewspaperCommand) -> None:
        self.__logger.info(f"Starting newspaper {command.newspaper_id} deletion")

        self.__newspaper_repository.delete(UUID(command.newspaper_id))

        self.__logger.info(f"Finished newspaper {command.newspaper_id} deletion")

    @classmethod
    def bus_stop_name(cls) -> str:
        return "command_handler.search_engine.delete_newspaper"
