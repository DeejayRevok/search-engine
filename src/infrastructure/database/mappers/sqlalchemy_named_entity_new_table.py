from sqlalchemy import Table, Column, ForeignKey

from infrastructure.database.mappers.sqlalchemy_table import SQLAlchemyTable


class SQLAlchemyNamedEntityNewTable(SQLAlchemyTable):
    def table(self) -> Table:
        return Table(
            "named_entity_new",
            self._metadata,
            Column("named_entity_value", ForeignKey("named_entity.value"), primary_key=True),
            Column("new_id", ForeignKey("new.id"), primary_key=True)
        )
