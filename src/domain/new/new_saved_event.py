from dataclasses import dataclass, field
from typing import Optional, List


@dataclass(frozen=True)
class NewSavedEvent:
    title: str
    url: str
    source: str
    date: float
    language: str
    entities: List[dict] = field(default_factory=list)
    sentiment: Optional[float] = None
