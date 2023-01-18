from logging import Logger
from typing import List, Iterable
from uuid import uuid4

from bus_station.command_terminal.command_handler import CommandHandler
from bus_station.event_terminal.bus.event_bus import EventBus

from application.create_newspaper.create_newspaper_command import CreateNewspaperCommand
from domain.named_entity.find_named_entities_criteria import FindNamedEntitiesCriteria
from domain.named_entity.named_entity import NamedEntity
from domain.named_entity.named_entity_repository import NamedEntityRepository
from domain.newspaper.newspaper import Newspaper
from domain.newspaper.newspaper_created_event import NewspaperCreatedEvent
from domain.newspaper.newspaper_repository import NewspaperRepository


class CreateNewspaperCommandHandler(CommandHandler):
    def __init__(
            self,
            newspaper_repository: NewspaperRepository,
            named_entity_repository: NamedEntityRepository,
            event_bus: EventBus,
            logger: Logger
    ):
        self.__newspaper_repository = newspaper_repository
        self.__named_entity_repository = named_entity_repository
        self.__event_bus = event_bus
        self.__logger = logger

    def handle(self, command: CreateNewspaperCommand) -> None:
        self.__logger.info(f"Starting newspaper {command.name} creation")

        newspaper = self.__create_newspaper_from_command(command)
        self.__newspaper_repository.save(newspaper)

        event = self.__create_event_from_newspaper(newspaper)
        self.__event_bus.transport(event)

        self.__logger.info(f"Finished newspaper {command.name} creation")

    def __create_newspaper_from_command(self, command: CreateNewspaperCommand) -> Newspaper:
        return Newspaper(
            id=uuid4(),
            name=command.name,
            user_email=command.user_email,
            named_entities=list(self.__get_named_entities(command.named_entities_values))
        )

    def __get_named_entities(self, named_entities_values: List[str]) -> Iterable[NamedEntity]:
        criteria = FindNamedEntitiesCriteria(
            value_in=named_entities_values
        )
        return self.__named_entity_repository.find_by_criteria(criteria)

    def __create_event_from_newspaper(self, newspaper: Newspaper) -> NewspaperCreatedEvent:
        return NewspaperCreatedEvent(
            id=str(newspaper.id),
            name=newspaper.name,
            user_email=newspaper.user_email,
        )

    @classmethod
    def bus_stop_name(cls) -> str:
        return "command_handler.search_engine.create_newspaper"
