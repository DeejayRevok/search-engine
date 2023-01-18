from dataclasses import dataclass
from typing import Optional


@dataclass
class NamedEntityType:
    name: str
    description: Optional[str]
