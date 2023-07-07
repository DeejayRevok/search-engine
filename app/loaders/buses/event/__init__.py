from app.loaders.buses.event.kombu_event_bus_loader import load as load_kombu_event_bus


def load() -> None:
    load_kombu_event_bus()
