from dataclasses import dataclass

from bus_station.event_terminal.event import Event


@dataclass(frozen=True)
class UserCreatedEvent(Event):
    email: str

    @classmethod
    def passenger_name(cls) -> str:
        return "event.user_created"
