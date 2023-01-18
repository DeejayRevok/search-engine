from dataclasses import dataclass

from bus_station.command_terminal.command import Command


@dataclass(frozen=True)
class SaveUserCommand(Command):
    email: str

    @classmethod
    def passenger_name(cls) -> str:
        return "command.search_engine.save_user"