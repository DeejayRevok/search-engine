from dataclasses import dataclass

from bus_station.command_terminal.command import Command


@dataclass(frozen=True)
class DeleteNewspaperCommand(Command):
    newspaper_id: str

    @classmethod
    def passenger_name(cls) -> str:
        return "command.search_engine.delete_newspaper"
