from decimal import Decimal
from logging import Logger
from uuid import uuid4

from bus_station.command_terminal.command_handler import CommandHandler
from bus_station.event_terminal.bus.event_bus import EventBus

from domain.named_entity.named_entity import NamedEntity
from domain.named_entity.named_entity_type import NamedEntityType
from domain.new.indexed_new_event import IndexedNewEvent
from domain.source.source import Source
from domain.new.new import New
from application.index_new.index_new_command import IndexNewCommand
from domain.new.new_repository import NewRepository


class IndexNewCommandHandler(CommandHandler):
    def __init__(self, new_repository: NewRepository, event_bus: EventBus, logger: Logger):
        self.__new_repository = new_repository
        self.__event_bus = event_bus
        self.__logger = logger

    def handle(self, command: IndexNewCommand) -> None:
        self.__logger.info(f"Starting index new {command.title}")

        new = self.__transform_command_to_new(command)
        self.__new_repository.save(new)

        event = self.__get_indexed_new_event(new)
        self.__event_bus.transport(event)

        self.__logger.info(f"Finished index new {command.title}")

    def __transform_command_to_new(self, command: IndexNewCommand) -> New:
        existing_new = self.__new_repository.find_by_title(command.title)
        new_id = existing_new.id if existing_new is not None else uuid4()
        return New(
            id=new_id,
            title=command.title,
            url=command.url,
            sentiment=Decimal(value=command.sentiment) if command.sentiment is not None else None,
            source=Source(name=command.source_name),
            named_entities=self.__transform_named_entity_dicts(command.named_entities)
        )

    def __transform_named_entity_dicts(self, named_entity_dicts: list[dict]) -> list[NamedEntity]:
        transformed_entities_values = set()
        transformed_entities = []

        for named_entity_dict in named_entity_dicts:
            named_entity = self.__transform_dict_to_named_entity(named_entity_dict)
            named_entity_value = named_entity.value
            if named_entity_value in transformed_entities_values:
                continue

            transformed_entities.append(named_entity)
            transformed_entities_values.add(named_entity_value)

        return transformed_entities

    def __transform_dict_to_named_entity(self, named_entity_dict: dict) -> NamedEntity:
        return NamedEntity(
            value=named_entity_dict["text"],
            named_entity_type=NamedEntityType(name=named_entity_dict["type"], description=None)
        )

    def __get_indexed_new_event(self, new: New) -> IndexedNewEvent:
        return IndexedNewEvent(
            title=new.title,
            url=new.url,
            sentiment=new.sentiment,
            source_name=new.source.name,
            named_entities=[{
                "value": named_entity.value,
                "type": named_entity.named_entity_type.name
            } for named_entity in new.named_entities]
        )

    @classmethod
    def bus_stop_name(cls) -> str:
        return "command_handler.search_engine.index_new"
