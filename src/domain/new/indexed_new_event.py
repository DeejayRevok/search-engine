from dataclasses import dataclass, field
from decimal import Decimal
from typing import List


@dataclass(frozen=True)
class IndexedNewEvent:
    title: str
    url: str
    sentiment: Decimal
    source_name: str
    named_entities: List[dict] = field(default_factory=list)
