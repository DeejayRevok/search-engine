from dataclasses import dataclass

from domain.named_entity.named_entity_type import NamedEntityType


@dataclass
class NamedEntity:
    value: str
    named_entity_type: NamedEntityType
