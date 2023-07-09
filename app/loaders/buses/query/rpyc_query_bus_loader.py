from bus_station.bus_stop.registration.address.redis_bus_stop_address_registry import RedisBusStopAddressRegistry
from bus_station.query_terminal.bus.synchronous.distributed.rpyc_query_bus import RPyCQueryBus
from bus_station.query_terminal.serialization.query_response_json_deserializer import QueryResponseJSONDeserializer
from yandil.container import default_container


def load() -> None:
    default_container.add(RedisBusStopAddressRegistry)
    default_container.add(QueryResponseJSONDeserializer)
    default_container.add(RPyCQueryBus)
