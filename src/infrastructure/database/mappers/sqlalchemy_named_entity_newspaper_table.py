from sqlalchemy import Table, Column, ForeignKey

from infrastructure.database.mappers.sqlalchemy_table import SQLAlchemyTable


class SQLAlchemyNamedEntityNewspaperTable(SQLAlchemyTable):
    def table(self) -> Table:
        return Table(
            "named_entity_newspaper",
            self._metadata,
            Column("named_entity_value", ForeignKey("named_entity.value", ondelete="CASCADE"), primary_key=True),
            Column("newspaper_id", ForeignKey("newspaper.id", ondelete="CASCADE"), primary_key=True),
        )
