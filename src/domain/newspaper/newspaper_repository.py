from abc import abstractmethod
from typing import Protocol, List, Iterable, Optional
from uuid import UUID

from domain.newspaper.find_newspaper_criteria import FindNewspaperCriteria
from domain.newspaper.newspaper import Newspaper


class NewspaperRepository(Protocol):
    @abstractmethod
    def save(self, newspaper: Newspaper) -> None:
        pass

    @abstractmethod
    def find_by_name_and_user_email(self, name: str, user_email: str) -> Optional[Newspaper]:
        pass

    @abstractmethod
    def find_by_criteria(self, criteria: FindNewspaperCriteria) -> Iterable[Newspaper]:
        pass

    @abstractmethod
    def delete(self, newspaper_id: UUID) -> None:
        pass
