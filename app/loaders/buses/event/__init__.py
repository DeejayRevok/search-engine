from app.loaders.buses.event.event_receiver_loader import load as load_event_receiver
from app.loaders.buses.event.kombu_event_bus_loader import load as load_kombu_event_bus


def load() -> None:
    load_event_receiver()
    load_kombu_event_bus()
