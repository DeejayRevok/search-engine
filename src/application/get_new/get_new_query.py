from dataclasses import dataclass

from bus_station.query_terminal.query import Query


@dataclass(frozen=True)
class GetNewQuery(Query):
    id: str

    @classmethod
    def passenger_name(cls) -> str:
        return "query.search_engine.get_new"
