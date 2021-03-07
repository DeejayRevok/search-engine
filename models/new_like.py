"""
New like database model definition module
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from models.new import New
from models.base import BASE


class NewLike(BASE):
    """
    New like relationship model
    """
    __tablename__ = 'new_like'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)

    new_id = Column(ForeignKey('new.id', ondelete='CASCADE'), nullable=False, index=True)

    new: New = relationship('New',
                            lazy='select',
                            uselist=False,
                            backref=backref('likes', lazy='select'))
