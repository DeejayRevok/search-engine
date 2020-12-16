from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from models.base import BASE

news_association = Table('new_noun_chunk', BASE.metadata,
                         Column('new_id', Integer, ForeignKey('new.id')),
                         Column('noun_chunk_id', Integer, ForeignKey('noun_chunk.id')))


class NounChunk(BASE):
    """
    Noun chunk model
    """
    __tablename__ = 'noun_chunk'

    id = Column(Integer, primary_key=True)
    value = Column(String(255), unique=True)

    news = relationship(
        "New",
        secondary=news_association,
        back_populates="noun_chunks")

    def __iter__(self) -> iter:
        """
        Iterate over the model properties

        Returns: iterator to the model properties

        """
        yield 'value', self.value
