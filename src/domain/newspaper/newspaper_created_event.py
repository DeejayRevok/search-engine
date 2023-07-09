from dataclasses import dataclass


@dataclass(frozen=True)
class NewspaperCreatedEvent:
    id: str
    name: str
    user_email: str
