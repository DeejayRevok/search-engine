from dataclasses import fields, MISSING
from json import loads
from typing import Generic, TypeVar, Optional, Type

from bus_station.passengers.passenger import Passenger
from bus_station.passengers.serialization.passenger_deserialization_error import PassengerDeserializationError
from bus_station.passengers.serialization.passenger_deserializer import PassengerDeserializer


P = TypeVar("P", bound=Passenger)


class IAMPassengerJSONDeserializer(PassengerDeserializer, Generic[P]):
    def deserialize(self, passenger_serialized: str, passenger_cls: Optional[Type[P]] = None) -> P:
        deserialized_data = self.__normalize_data(loads(passenger_serialized))
        if passenger_cls is None:
            raise ValueError(f"Missing passenger class for deserializing {passenger_serialized}")
        return self.__from_passenger_cls(passenger_cls, deserialized_data)

    def __normalize_data(self, data: dict) -> dict:
        return {key.lower(): value for key, value in data.items()}

    def __from_passenger_cls(self, passenger_cls: Type[P], passenger_data: dict) -> P:
        passenger_cls_field_values = dict()
        for passenger_field in fields(passenger_cls):
            if passenger_field.default is MISSING and passenger_field.name not in passenger_data:
                raise PassengerDeserializationError(passenger_cls, f"Missing value for field {passenger_field.name}")
            if passenger_field.name not in passenger_data:
                continue
            passenger_cls_field_values[passenger_field.name] = passenger_data[passenger_field.name]
        return passenger_cls(**passenger_cls_field_values)
