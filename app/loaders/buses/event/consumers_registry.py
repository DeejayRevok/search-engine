from bus_station.event_terminal.registry.event_registry import EventRegistry
from pypendency.builder import container_builder

from domain.new.new_saved_event import NewSavedEvent
from domain.user.user_created_event import UserCreatedEvent


def register() -> None:
    registry: EventRegistry = container_builder.get(
        "bus_station.event_terminal.registry.redis_event_registry.RedisEventRegistry"
    )

    user_created_event_consumer = container_builder.get(
        "application.save_user.user_created_event_consumer.UserCreatedEventConsumer"
    )
    new_saved_event_consumer = container_builder.get(
        "application.index_new.new_saved_event_consumer.NewSavedEventConsumer"
    )
    registry.register(user_created_event_consumer, UserCreatedEvent.passenger_name())
    registry.register(new_saved_event_consumer, NewSavedEvent.passenger_name())
