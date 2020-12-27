"""
Named entity type database model definition module
"""
from sqlalchemy import Column, Integer, String

from models.base import BASE


class NamedEntityType(BASE):
    """
    Named entity type model
    """
    __tablename__ = 'named_entity_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(255))

    def __iter__(self) -> iter:
        """
        Iterate over the model properties

        Returns: iterator to the model properties

        """
        yield 'name', self.name
        yield 'description', self.description
