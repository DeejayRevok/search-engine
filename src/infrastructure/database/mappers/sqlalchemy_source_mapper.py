from typing import Type

from sqlalchemy import Table, Column, String

from domain.source.source import Source
from infrastructure.database.mappers.sqlalchemy_mapper import SQLAlchemyMapper


class SQLAlchemySourceMapper(SQLAlchemyMapper):
    def model(self) -> Type:
        return Source

    def table(self) -> Table:
        return Table("source", self._metadata, Column("name", String(), primary_key=True))
