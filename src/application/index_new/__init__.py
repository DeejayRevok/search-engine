from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.index_new.new_saved_event_consumer.NewSavedEventConsumer",
            "application.index_new.new_saved_event_consumer.NewSavedEventConsumer",
            [
                Argument.no_kw_argument("@bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus")
            ]
        )
    )
    container_builder.set_definition(
        Definition(
            "application.index_new.index_new_command_handler.IndexNewCommandHandler",
            "application.index_new.index_new_command_handler.IndexNewCommandHandler",
            [
                Argument.no_kw_argument("@infrastructure.database.repositories.sqlalchemy_new_repository.SQLAlchemyNewRepository"),
                Argument.no_kw_argument(
                    "@bus_station.event_terminal.bus.asynchronous.distributed.kombu_event_bus.KombuEventBus"),
                Argument.no_kw_argument("@logging.Logger")
            ]
        )
    )
