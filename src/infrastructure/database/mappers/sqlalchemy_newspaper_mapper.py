from typing import Type

from sqlalchemy import Table, Column, String, ForeignKey, MetaData, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from domain.named_entity.named_entity import NamedEntity
from domain.newspaper.newspaper import Newspaper
from infrastructure.database.mappers.sqlalchemy_mapper import SQLAlchemyMapper
from infrastructure.database.mappers.sqlalchemy_named_entity_newspaper_table import SQLAlchemyNamedEntityNewspaperTable


class SQLAlchemyNewspaperMapper(SQLAlchemyMapper):
    def __init__(
        self, sql_alchemy_metadata: MetaData, named_entities_association_table: SQLAlchemyNamedEntityNewspaperTable
    ):
        super().__init__(sql_alchemy_metadata)
        self.__named_entities_association_table = named_entities_association_table.table()

    def model(self) -> Type:
        return Newspaper

    def table(self) -> Table:
        return Table(
            "newspaper",
            self._metadata,
            Column("id", UUID(as_uuid=True), primary_key=True),
            Column("name", String(), nullable=False),
            Column("user_email", ForeignKey("users.email"), nullable=False),
            UniqueConstraint("name", "user_email"),
        )

    def mapping_properties(self) -> dict:
        return {
            "named_entities": relationship(
                NamedEntity, secondary=self.__named_entities_association_table, cascade="all"
            ),
        }
