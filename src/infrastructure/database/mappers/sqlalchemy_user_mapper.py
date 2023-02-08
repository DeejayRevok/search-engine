from typing import Type

from sqlalchemy import Table, Column, String

from domain.user.user import User
from infrastructure.database.mappers.sqlalchemy_mapper import SQLAlchemyMapper


class SQLAlchemyUserMapper(SQLAlchemyMapper):
    def model(self) -> Type:
        return User

    def table(self) -> Table:
        return Table(
            "users",
            self._metadata,
            Column("email", String(320), primary_key=True),
        )
