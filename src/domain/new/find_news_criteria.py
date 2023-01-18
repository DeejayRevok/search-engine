from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class FindNewsCriteria:
    title: Optional[str] = None
    any_named_entity_value: Optional[List[str]] = None
    all_named_entities_values: Optional[List[str]] = None
    source_name: Optional[str] = None
