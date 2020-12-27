"""
Search field module
"""
from enum import Enum
from typing import Any

from sqlalchemy.orm import Query

from models import New, NamedEntity, NounChunk


class SearchField(Enum):
    """
    Search fields definition:
    - NAMED_ENTITY: named entity search field
    - NOUN_CHUNK: noun chunk search field
    """
    NAMED_ENTITY = ('value', 'named_entities', NamedEntity)
    NOUN_CHUNK = ('value', 'noun_chunks', NounChunk)

    @property
    def destination_field(self) -> str:
        """
        Get the destination field

        Returns: name of the destination field

        """
        return self.value[0]

    @property
    def new_join_field(self) -> str:
        """
        Get the join field

        Returns: name of the joining field in the new entity

        """
        return self.value[1]

    @property
    def destination_entity(self) -> str:
        """
        Get the destination entity

        Returns: class of the destination entity

        """
        return self.value[2]

    def query(self, base_query: Query, field_value: Any) -> Query:
        """
        Get the current field query

        Args:
            base_query: base query used for building the query
            field_value: value of the field filter

        Returns: field query

        """
        return base_query.join(getattr(New, self.new_join_field)).filter(
            getattr(self.destination_entity, self.destination_field) == field_value)
