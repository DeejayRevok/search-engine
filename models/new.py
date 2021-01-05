"""
New database model definition module
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref

from models import Source
from models.base import BASE
from models.named_entity import news_association as named_entities_association
from models.noun_chunk import news_association as noun_chunk_association


class New(BASE):
    """
    New model
    """
    __tablename__ = 'new'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    url = Column(String(2083), unique=True, nullable=False)
    sentiment = Column(Float)
    source_id = Column(ForeignKey('source.id'), nullable=False, index=True)

    source: Source = relationship('Source',
                                  lazy='select',
                                  uselist=False,
                                  backref=backref('news', lazy='select'))
    noun_chunks = relationship(
        "NounChunk",
        secondary=noun_chunk_association,
        back_populates="news")

    named_entities = relationship(
        "NamedEntity",
        secondary=named_entities_association,
        back_populates="news")

    def __iter__(self) -> iter:
        """
        Iterate over the model properties

        Returns: iterator to the model properties

        """
        yield 'title', self.title
        yield 'sentiment', self.sentiment
        yield 'url', self.url
