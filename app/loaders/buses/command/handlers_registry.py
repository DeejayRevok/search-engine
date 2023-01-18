from bus_station.command_terminal.registry.command_registry import CommandRegistry
from pypendency.builder import container_builder


def register() -> None:
    registry: CommandRegistry = container_builder.get(
        "bus_station.command_terminal.registry.in_memory_command_registry.InMemoryCommandRegistry"
    )

    command_handler_fqns = [
        "application.create_newspaper.create_newspaper_command_handler.CreateNewspaperCommandHandler",
        "application.delete_newspaper.delete_newspaper_command_handler.DeleteNewspaperCommandHandler",
        "application.index_new.index_new_command_handler.IndexNewCommandHandler",
        "application.save_user.save_user_command_handler.SaveUserCommandHandler",
        "application.update_newspaper.update_newspaper_command_handler.UpdateNewspaperCommandHandler",
    ]
    for command_handler_fqn in command_handler_fqns:
        command_handler = container_builder.get(command_handler_fqn)
        registry.register(command_handler, command_handler)
