from bus_station.command_terminal.command_handler_registry import CommandHandlerRegistry
from yandil.container import default_container

from application.create_newspaper.create_newspaper_command_handler import CreateNewspaperCommandHandler
from application.delete_newspaper.delete_newspaper_command_handler import DeleteNewspaperCommandHandler
from application.index_new.index_new_command_handler import IndexNewCommandHandler
from application.save_user.save_user_command_handler import SaveUserCommandHandler
from application.update_newspaper.update_newspaper_command_handler import UpdateNewspaperCommandHandler


def register() -> None:
    registry = default_container[CommandHandlerRegistry]

    command_handlers = [
        CreateNewspaperCommandHandler,
        DeleteNewspaperCommandHandler,
        IndexNewCommandHandler,
        SaveUserCommandHandler,
        UpdateNewspaperCommandHandler,
    ]
    for command_handler in command_handlers:
        registry.register(command_handler)
