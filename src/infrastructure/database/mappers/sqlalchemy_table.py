from abc import ABC, abstractmethod

from sqlalchemy import MetaData, Table


class SQLAlchemyTable(ABC):
    def __init__(self, sqlalchemy_metadata: MetaData):
        self._metadata = sqlalchemy_metadata

    @abstractmethod
    def table(self) -> Table:
        pass
