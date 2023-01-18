from dataclasses import dataclass
from typing import List

from bus_station.command_terminal.command import Command


@dataclass(frozen=True)
class CreateNewspaperCommand(Command):
    name: str
    user_email: str
    named_entities_values: List[str]

    @classmethod
    def passenger_name(cls) -> str:
        return "command.search_engine.create_newspaper"
