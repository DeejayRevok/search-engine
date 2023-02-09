from dataclasses import dataclass

from bus_station.event_terminal.event import Event


@dataclass(frozen=True)
class NewspaperCreatedEvent(Event):
    id: str
    name: str
    user_email: str

    @classmethod
    def passenger_name(cls) -> str:
        return "event.newspaper_created"
