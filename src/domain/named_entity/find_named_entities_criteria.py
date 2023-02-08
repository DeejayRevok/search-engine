from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class FindNamedEntitiesCriteria:
    value_in: List[str] = None
