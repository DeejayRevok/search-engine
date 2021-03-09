"""
Source database model definition module
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import BASE
from models.user import source_follows


class Source(BASE):
    """
    News source model
    """
    __tablename__ = 'source'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    follows = relationship(
        "User",
        secondary=source_follows,
        back_populates="source_follows")

    def __iter__(self) -> iter:
        """
        Iterate over the model properties

        Returns: iterator to the model properties

        """
        yield 'name', self.name
