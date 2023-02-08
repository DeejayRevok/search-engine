from abc import abstractmethod
from typing import Protocol, Optional

from infrastructure.jwt.jwt_signing_key import JWTSigningKey


class JWTSigningKeyFetcher(Protocol):
    @abstractmethod
    def fetch(self) -> Optional[JWTSigningKey]:
        pass
