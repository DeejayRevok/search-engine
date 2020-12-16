from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from models.base import BASE
from models.source import Source


class UserSource(BASE):
    """
    User news source relationship model
    """
    __tablename__ = 'user_source'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))

    source_id = Column(ForeignKey('source.id'), nullable=False, index=True)

    source: Source = relationship('Source',
                                  lazy='select',
                                  uselist=False,
                                  backref=backref('user_sources', lazy='select'))
