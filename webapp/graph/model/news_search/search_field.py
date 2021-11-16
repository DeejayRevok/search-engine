from enum import Enum
from typing import Any

from sqlalchemy.orm import Query

from models.named_entity import NamedEntity
from models.new import New
from models.noun_chunk import NounChunk


class SearchField(Enum):
    NAMED_ENTITY = ('value', 'named_entities', NamedEntity)
    NOUN_CHUNK = ('value', 'noun_chunks', NounChunk)

    @property
    def destination_field(self) -> str:
        return self.value[0]

    @property
    def new_join_field(self) -> str:
        return self.value[1]

    @property
    def destination_entity(self) -> str:
        return self.value[2]

    def query(self, base_query: Query, field_value: Any) -> Query:
        return base_query.join(getattr(New, self.new_join_field)).filter(
            getattr(self.destination_entity, self.destination_field) == field_value)
