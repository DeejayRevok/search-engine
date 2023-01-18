from dataclasses import dataclass
from typing import List

from bus_station.command_terminal.command import Command


@dataclass(frozen=True)
class UpdateNewspaperCommand(Command):
    user_email: str
    original_name: str
    new_name: str
    new_named_entities_values: List[str]

    @classmethod
    def passenger_name(cls) -> str:
        return "command.search_engine.update_newspaper"
