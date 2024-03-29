from argparse import ArgumentParser
from importlib import import_module
from typing import Dict, Optional

from bus_station.event_terminal.bus_engine.kombu_event_bus_engine import KombuEventBusEngine
from bus_station.event_terminal.event_consumer_registry import EventConsumerRegistry
from bus_station.event_terminal.middleware.event_middleware_receiver import EventMiddlewareReceiver
from bus_station.passengers.serialization.passenger_deserializer import PassengerDeserializer
from bus_station.passengers.serialization.passenger_json_deserializer import PassengerJSONDeserializer
from bus_station.shared_terminal.engine.runner.self_process_engine_runner import SelfProcessEngineRunner
from kombu.connection import Connection
from yandil.container import default_container

from app.loaders import load_app


def run() -> None:
    load_app()
    args = __load_args()
    engine = KombuEventBusEngine(
        broker_connection=default_container[Connection],
        event_receiver=default_container[EventMiddlewareReceiver],
        event_consumer_registry=default_container[EventConsumerRegistry],
        event_deserializer=__get_passenger_deserializer(args["deserializer"]),
        event_consumer_name=args["consumer"],
    )
    SelfProcessEngineRunner(engine).run()


def __get_passenger_deserializer(deserializer_fqn: Optional[str]) -> PassengerDeserializer:
    if deserializer_fqn is None:
        return default_container[PassengerJSONDeserializer]

    module_name, class_qualname = deserializer_fqn.rsplit(".", 1)
    module = import_module(module_name)
    deserializer_class = getattr(module, class_qualname)
    return default_container[deserializer_class]


def __load_args() -> Dict:
    arg_solver = ArgumentParser(description="Event consumer runner")
    arg_solver.add_argument("-c", "--consumer", required=True, help="Event consumer name")
    arg_solver.add_argument("-d", "--deserializer", required=False, help="Event deserializer", default=None)

    return vars(arg_solver.parse_args())


if __name__ == "__main__":
    run()
