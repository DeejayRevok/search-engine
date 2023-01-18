from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.save_user.user_created_event_consumer.UserCreatedEventConsumer",
            "application.save_user.user_created_event_consumer.UserCreatedEventConsumer",
            [
                Argument.no_kw_argument(
                    "@bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus"
                ),
            ]
        )
    )
    container_builder.set_definition(
        Definition(
            "application.save_user.save_user_command_handler.SaveUserCommandHandler",
            "application.save_user.save_user_command_handler.SaveUserCommandHandler",
            [
                Argument.no_kw_argument("@infrastructure.database.repositories.sqlalchemy_user_repository.SQLAlchemyUserRepository"),
                Argument.no_kw_argument("@logging.Logger")
            ]
        )
    )
