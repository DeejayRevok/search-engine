from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref

from models.source import Source
from models.base import BASE
from models.named_entity import news_association as named_entities_association
from models.noun_chunk import news_association as noun_chunk_association
from models.user import user_news, new_likes


class New(BASE):
    __tablename__ = "new"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    url = Column(String(2083), nullable=False)
    sentiment = Column(Float)
    source_id = Column(ForeignKey("source.id"), nullable=False, index=True)

    source: Source = relationship("Source", lazy="select", uselist=False, backref=backref("news", lazy="select"))
    noun_chunks = relationship("NounChunk", secondary=noun_chunk_association, back_populates="news")

    named_entities = relationship("NamedEntity", secondary=named_entities_association, back_populates="news")

    archived_by = relationship("User", secondary=user_news, back_populates="news")

    likes = relationship("User", secondary=new_likes, back_populates="new_likes")

    def __iter__(self) -> iter:
        yield "title", self.title
        yield "sentiment", self.sentiment
        yield "url", self.url
