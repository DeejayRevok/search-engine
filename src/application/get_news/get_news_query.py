from dataclasses import dataclass
from typing import List, Optional

from bus_station.query_terminal.query import Query


@dataclass(frozen=True)
class GetNewsQuery(Query):
    title: Optional[str] = None
    any_named_entity: Optional[List[str]] = None
    all_named_entities: Optional[List[str]] = None
    source: Optional[str] = None
    sorting: Optional[str] = None

    @classmethod
    def passenger_name(cls) -> str:
        return "query.search_engine.get_news"
