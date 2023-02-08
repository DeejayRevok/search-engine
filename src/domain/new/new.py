from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from domain.source.source import Source
from domain.named_entity.named_entity import NamedEntity


@dataclass
class New:
    id: UUID
    title: str
    url: str
    sentiment: Optional[Decimal]
    source: Source
    named_entities: List[NamedEntity] = field(default_factory=list)
