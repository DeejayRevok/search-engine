from bus_station.event_terminal.event_consumer_registry import EventConsumerRegistry
from yandil.container import default_container

from application.index_new.new_saved_event_consumer import NewSavedEventConsumer
from application.save_user.user_created_event_consumer import UserCreatedEventConsumer


def register() -> None:
    registry = default_container[EventConsumerRegistry]

    registry.register(UserCreatedEventConsumer)
    registry.register(NewSavedEventConsumer)
