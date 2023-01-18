from typing import Type

from sqlalchemy import Table, Column, String

from domain.named_entity.named_entity_type import NamedEntityType
from infrastructure.database.mappers.sqlalchemy_mapper import SQLAlchemyMapper


class SQLAlchemyNamedEntityTypeMapper(SQLAlchemyMapper):
    def model(self) -> Type:
        return NamedEntityType

    def table(self) -> Table:
        return Table(
            "named_entity_type",
            self._metadata,
            Column("name", String(), primary_key=True),
            Column("description", String(), nullable=True)
        )
