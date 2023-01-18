from abc import abstractmethod
from typing import Protocol, Iterable

from domain.named_entity.find_named_entities_criteria import FindNamedEntitiesCriteria
from domain.named_entity.named_entity import NamedEntity


class NamedEntityRepository(Protocol):
    @abstractmethod
    def find_by_criteria(self, criteria: FindNamedEntitiesCriteria) -> Iterable[NamedEntity]:
        pass
