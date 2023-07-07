from bus_station.command_terminal.command_handler_registry import CommandHandlerRegistry
from yandil.container import default_container


def register() -> None:
    registry = default_container[CommandHandlerRegistry]

    command_handler_fqns = [
        "application.create_newspaper.create_newspaper_command_handler.CreateNewspaperCommandHandler",
        "application.delete_newspaper.delete_newspaper_command_handler.DeleteNewspaperCommandHandler",
        "application.index_new.index_new_command_handler.IndexNewCommandHandler",
        "application.save_user.save_user_command_handler.SaveUserCommandHandler",
        "application.update_newspaper.update_newspaper_command_handler.UpdateNewspaperCommandHandler",
    ]
    for command_handler_fqn in command_handler_fqns:
        registry.register(command_handler_fqn)
