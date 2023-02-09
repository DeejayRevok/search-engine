from argparse import ArgumentParser
from typing import Dict, Optional

from bus_station.event_terminal.bus_engine.kombu_event_bus_engine import KombuEventBusEngine
from bus_station.passengers.serialization.passenger_deserializer import PassengerDeserializer
from bus_station.shared_terminal.engine.runner.self_process_engine_runner import SelfProcessEngineRunner
from pypendency.builder import container_builder

from app.loaders import load_app


def run() -> None:
    load_app()
    args = __load_args()
    engine = KombuEventBusEngine(
        container_builder.get("kombu.connection.Connection"),
        container_builder.get("bus_station.event_terminal.registry.redis_event_registry.RedisEventRegistry"),
        container_builder.get(
            "bus_station.event_terminal.middleware.event_middleware_receiver.EventMiddlewareReceiver"
        ),
        __get_passenger_deserializer(args["deserializer"]),
        args["event"],
        args["consumer"],
    )
    SelfProcessEngineRunner(engine).run()


def __get_passenger_deserializer(deserializer_fqn: Optional[str]) -> PassengerDeserializer:
    if deserializer_fqn is None:
        return container_builder.get(
            "bus_station.passengers.serialization.passenger_json_deserializer.PassengerJSONDeserializer"
        )
    return container_builder.get(deserializer_fqn)


def __load_args() -> Dict:
    arg_solver = ArgumentParser(description="Event consumer runner")
    arg_solver.add_argument("-e", "--event", required=True, help="Event name")
    arg_solver.add_argument("-c", "--consumer", required=True, help="Event consumer name")
    arg_solver.add_argument("-d", "--deserializer", required=False, help="Event deserializer", default=None)

    return vars(arg_solver.parse_args())


if __name__ == "__main__":
    run()
