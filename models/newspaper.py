"""
Newspaper database model definition module
"""
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from models.base import BASE

named_entities_association = Table('newspaper_named_entity', BASE.metadata,
                                   Column('newspaper_id', Integer, ForeignKey('newspaper.id', ondelete='CASCADE')),
                                   Column('named_entity_id', Integer,
                                          ForeignKey('named_entity.id', ondelete='CASCADE')))

noun_chunks_association = Table('newspaper_noun_chunk', BASE.metadata,
                                Column('newspaper_id', Integer, ForeignKey('newspaper.id', ondelete='CASCADE')),
                                Column('noun_chunk_id', Integer, ForeignKey('noun_chunk.id', ondelete='CASCADE')))


class Newspaper(BASE):
    """
    Newspaper model
    """
    __tablename__ = 'newspaper'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)

    named_entities = relationship("NamedEntity",
                                  secondary=named_entities_association,
                                  back_populates="newspapers")

    noun_chunks = relationship("NounChunk",
                               secondary=noun_chunks_association,
                               back_populates="newspapers")

    def __iter__(self) -> iter:
        """
        Iterate over the model properties

        Returns: iterator to the model properties

        """
        yield 'name', self.name
