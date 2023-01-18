from typing import Type

from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from domain.named_entity.named_entity import NamedEntity
from domain.named_entity.named_entity_type import NamedEntityType
from infrastructure.database.mappers.sqlalchemy_mapper import SQLAlchemyMapper


class SQLAlchemyNamedEntityMapper(SQLAlchemyMapper):
    def model(self) -> Type:
        return NamedEntity

    def table(self) -> Table:
        return Table(
            "named_entity",
            self._metadata,
            Column("value", String(), primary_key=True),
            Column("named_entity_type_name", ForeignKey("named_entity_type.name"), nullable=False),
        )

    def mapping_properties(self) -> dict:
        return {
            "named_entity_type": relationship(NamedEntityType),
        }
