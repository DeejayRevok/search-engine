from app.loaders.buses.query.sync_query_bus_loader import load as load_sync_query_bus
from app.loaders.buses.query.rpyc_query_bus_loader import load as load_rpyc_query_bus


def load() -> None:
    load_sync_query_bus()
    load_rpyc_query_bus()
