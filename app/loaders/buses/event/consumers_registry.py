from bus_station.event_terminal.event_consumer_registry import EventConsumerRegistry
from yandil.container import default_container


def register() -> None:
    registry = default_container[EventConsumerRegistry]

    registry.register("application.save_user.user_created_event_consumer.UserCreatedEventConsumer")
    registry.register("application.index_new.new_saved_event_consumer.NewSavedEventConsumer")
