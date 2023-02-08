from bus_station.command_terminal.bus.command_bus import CommandBus
from bus_station.event_terminal.event_consumer import EventConsumer

from application.save_user.save_user_command import SaveUserCommand
from domain.user.user_created_event import UserCreatedEvent


class UserCreatedEventConsumer(EventConsumer):
    def __init__(self, command_bus: CommandBus):
        self.__command_bus = command_bus

    def consume(self, event: UserCreatedEvent) -> None:
        self.__command_bus.transport(SaveUserCommand(email=event.email))

    @classmethod
    def bus_stop_name(cls) -> str:
        return "event_consumer.search_engine.save_user.user_created"
