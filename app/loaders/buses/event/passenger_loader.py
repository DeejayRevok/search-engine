from bus_station.event_terminal.event import Event
from bus_station.passengers.passenger_mapper import passenger_mapper

from domain.new.indexed_new_event import IndexedNewEvent
from domain.new.new_saved_event import NewSavedEvent
from domain.newspaper.newspaper_created_event import NewspaperCreatedEvent
from domain.user.user_created_event import UserCreatedEvent


def load() -> None:
    passenger_mapper(IndexedNewEvent, Event, "event.indexed_new")
    passenger_mapper(NewSavedEvent, Event, "event.new_saved")
    passenger_mapper(NewspaperCreatedEvent, Event, "event.newspaper_created")
    passenger_mapper(UserCreatedEvent, Event, "event.user_created")
