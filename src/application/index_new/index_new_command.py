from dataclasses import dataclass, field
from typing import List

from bus_station.command_terminal.command import Command


@dataclass(frozen=True)
class IndexNewCommand(Command):
    title: str
    url: str
    sentiment: float
    source_name: str
    named_entities: List[dict] = field(default_factory=list)

    @classmethod
    def passenger_name(cls) -> str:
        return "command.search_engine.index_new"