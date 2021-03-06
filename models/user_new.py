"""
User new database model definition module
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from models import New
from models.base import BASE


class UserNew(BASE):
    """
    User news relationship model
    """
    __tablename__ = 'user_new'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)

    new_id = Column(ForeignKey('new.id', ondelete='CASCADE'), nullable=False, index=True)

    new: New = relationship('New',
                            lazy='select',
                            uselist=False,
                            backref=backref('user_news', lazy='select'))
