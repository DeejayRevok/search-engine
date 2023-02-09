from logging import Logger
from typing import List, Iterable

from bus_station.command_terminal.command_handler import CommandHandler

from application.update_newspaper.update_newspaper_command import UpdateNewspaperCommand
from domain.named_entity.find_named_entities_criteria import FindNamedEntitiesCriteria
from domain.named_entity.named_entity import NamedEntity
from domain.named_entity.named_entity_repository import NamedEntityRepository
from domain.newspaper.newspaper_repository import NewspaperRepository


class UpdateNewspaperCommandHandler(CommandHandler):
    def __init__(
        self, newspaper_repository: NewspaperRepository, named_entity_repository: NamedEntityRepository, logger: Logger
    ):
        self.__newspaper_repository = newspaper_repository
        self.__named_entity_repository = named_entity_repository
        self.__logger = logger

    def handle(self, command: UpdateNewspaperCommand) -> None:
        self.__logger.info(f"Starting newspaper {command.original_name} update")

        newspaper = self.__newspaper_repository.find_by_name_and_user_email(
            name=command.original_name, user_email=command.user_email
        )

        if (new_name := command.new_name) is not None:
            newspaper.name = new_name

        if (new_named_entities_values := command.new_named_entities_values) is not None:
            new_named_entities = self.__get_named_entities(new_named_entities_values)
            newspaper.named_entities = new_named_entities

        self.__newspaper_repository.save(newspaper)
        self.__logger.info(f"Finished newspaper {command.original_name} update")

    def __get_named_entities(self, named_entities_values: List[str]) -> Iterable[NamedEntity]:
        criteria = FindNamedEntitiesCriteria(value_in=named_entities_values)
        return self.__named_entity_repository.find_by_criteria(criteria)

    @classmethod
    def bus_stop_name(cls) -> str:
        return "command_handler.search_engine.update_newspaper"
