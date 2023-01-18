from dataclasses import dataclass, field
from typing import Optional, List

from bus_station.event_terminal.event import Event


@dataclass(frozen=True)
class NewSavedEvent(Event):
    title: str
    url: str
    source: str
    date: float
    language: str
    entities: List[dict] = field(default_factory=list)
    sentiment: Optional[float] = None

    @classmethod
    def passenger_name(cls) -> str:
        return "event.new_saved"