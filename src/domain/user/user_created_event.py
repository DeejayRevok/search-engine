from dataclasses import dataclass


@dataclass(frozen=True)
class UserCreatedEvent:
    email: str
