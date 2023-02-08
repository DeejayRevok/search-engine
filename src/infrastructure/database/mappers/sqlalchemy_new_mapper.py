from typing import Type

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData, Table, Column, String, Numeric, ForeignKey

from domain.source.source import Source
from domain.named_entity.named_entity import NamedEntity
from domain.new.new import New
from infrastructure.database.mappers.sqlalchemy_mapper import SQLAlchemyMapper
from infrastructure.database.mappers.sqlalchemy_named_entity_new_table import SQLAlchemyNamedEntityNewTable


class SQLAlchemyNewMapper(SQLAlchemyMapper):
    def __init__(self, sql_alchemy_metadata: MetaData, named_entities_association_table: SQLAlchemyNamedEntityNewTable):
        super().__init__(sql_alchemy_metadata)
        self.__named_entities_association_table = named_entities_association_table.table()

    def model(self) -> Type:
        return New

    def table(self) -> Table:
        return Table(
            "new",
            self._metadata,
            Column("id", UUID(as_uuid=True), primary_key=True),
            Column("title", String(), nullable=False),
            Column("url", String(), nullable=False),
            Column("sentiment", Numeric(asdecimal=True), nullable=True),
            Column("source_name", ForeignKey("source.name"), nullable=False),
        )

    def mapping_properties(self) -> dict:
        return {
            "named_entities": relationship(
                NamedEntity, secondary=self.__named_entities_association_table, cascade="all"
            ),
            "source": relationship(Source),
        }
