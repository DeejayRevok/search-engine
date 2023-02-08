from abc import abstractmethod
from typing import Protocol

from domain.authentication.authentication_token import AuthenticationToken


class AuthenticationTokenDecoder(Protocol):
    @abstractmethod
    def decode(self, token_encoded: str) -> AuthenticationToken:
        pass
