"""
Newspaper follow database model definition module
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from models import Newspaper
from models.base import BASE


class NewspaperFollow(BASE):
    """
    Newspaper follow relationship model
    """
    __tablename__ = 'newspaper_follow'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)

    newspaper_id = Column(ForeignKey('newspaper.id', ondelete='CASCADE'), nullable=False, index=True)

    newspaper: Newspaper = relationship('Newspaper',
                                        lazy='select',
                                        uselist=False,
                                        backref=backref('follows', lazy='select'))
