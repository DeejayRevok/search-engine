from abc import abstractmethod
from typing import Protocol

from domain.user.user import User


class UserRepository(Protocol):
    @abstractmethod
    def save(self, user: User) -> None:
        pass
