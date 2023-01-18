from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.create_newspaper.create_newspaper_command_handler.CreateNewspaperCommandHandler",
            "application.create_newspaper.create_newspaper_command_handler.CreateNewspaperCommandHandler",
            [
                Argument.no_kw_argument("@infrastructure.database.repositories.sqlalchemy_newspaper_repository.SQLAlchemyNewspaperRepository"),
                Argument.no_kw_argument("@infrastructure.database.repositories.sqlalchemy_named_entity_repository.SQLAlchemyNamedEntityRepository"),
                Argument.no_kw_argument(
                    "@bus_station.event_terminal.bus.asynchronous.distributed.kombu_event_bus.KombuEventBus"),
                Argument.no_kw_argument("@logging.Logger")
            ]
        )
    )
