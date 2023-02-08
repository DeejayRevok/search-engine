from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from bus_station.event_terminal.event import Event


@dataclass(frozen=True)
class IndexedNewEvent(Event):
    title: str
    url: str
    sentiment: Decimal
    source_name: str
    named_entities: List[dict] = field(default_factory=list)

    @classmethod
    def passenger_name(cls) -> str:
        return "event.indexed_new"
