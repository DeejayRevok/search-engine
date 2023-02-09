from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from domain.named_entity.named_entity import NamedEntity


@dataclass
class Newspaper:
    id: UUID
    name: str
    user_email: str
    named_entities: List[NamedEntity] = field(default_factory=list)
