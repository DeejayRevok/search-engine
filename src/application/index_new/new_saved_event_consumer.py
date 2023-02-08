from bus_station.command_terminal.bus.command_bus import CommandBus
from bus_station.event_terminal.event_consumer import EventConsumer

from application.index_new.index_new_command import IndexNewCommand
from domain.new.new_saved_event import NewSavedEvent


class NewSavedEventConsumer(EventConsumer):
    def __init__(self, command_bus: CommandBus):
        self.__command_bus = command_bus

    def consume(self, event: NewSavedEvent) -> None:
        index_new_command = IndexNewCommand(
            title=event.title,
            url=event.url,
            sentiment=event.sentiment,
            source_name=event.source,
            named_entities=event.entities,
        )
        self.__command_bus.transport(index_new_command)

    @classmethod
    def bus_stop_name(cls) -> str:
        return "event_consumer.search_engine.index_new.new_saved"
