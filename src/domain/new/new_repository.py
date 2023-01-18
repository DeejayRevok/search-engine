from abc import abstractmethod
from typing import Protocol, Iterable, Optional
from uuid import UUID

from domain.new.find_news_criteria import FindNewsCriteria
from domain.new.new import New
from domain.new.sort_news_criteria import SortNewsCriteria


class NewRepository(Protocol):
    @abstractmethod
    def save(self, new: New) -> None:
        pass

    @abstractmethod
    def find_by_criteria(
            self, criteria: FindNewsCriteria, sort_criteria: Optional[SortNewsCriteria] = None
    ) -> Iterable[New]:
        pass

    @abstractmethod
    def find_by_id(self, new_id: UUID) -> Optional[New]:
        pass

    @abstractmethod
    def find_by_title(self, new_title: str) -> Optional[New]:
        pass
