from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class FindNamedEntitiesCriteria:
    value_in: Optional[List[str]] = None
