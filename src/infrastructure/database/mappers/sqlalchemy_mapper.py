from abc import abstractmethod, ABC
from typing import Type

from sqlalchemy import MetaData, Table
from sqlalchemy.orm import mapper


class SQLAlchemyMapper(ABC):
    def __init__(self, sql_alchemy_metadata: MetaData):
        self._metadata = sql_alchemy_metadata

    @abstractmethod
    def model(self) -> Type:
        pass

    @abstractmethod
    def table(self) -> Table:
        pass

    def mapping_properties(self) -> dict:
        return {}

    def map(self):
        mapper(self.model(), self.table(), self.mapping_properties())
