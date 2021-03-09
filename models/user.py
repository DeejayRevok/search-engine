"""
User view database model definition module
"""
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from models.base import BASE

newspaper_follows = Table('newspaper_follow', BASE.metadata,
                          Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
                          Column('newspaper_id', Integer, ForeignKey('newspaper.id', ondelete='CASCADE')),)

user_news = Table('user_new', BASE.metadata,
                  Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
                  Column('new_id', Integer, ForeignKey('new.id', ondelete='CASCADE')),)

new_likes = Table('new_like', BASE.metadata,
                  Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
                  Column('new_id', Integer, ForeignKey('new.id', ondelete='CASCADE')),)

source_follows = Table('source_follow', BASE.metadata,
                       Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
                       Column('source_id', Integer, ForeignKey('source.id', ondelete='CASCADE')),)


class User(BASE):
    """
    User view database model
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String(255), nullable=False)

    newspapers = relationship("Newspaper",
                              lazy="select")

    newspaper_follows = relationship("Newspaper",
                                     secondary=newspaper_follows,
                                     back_populates="follows")

    news = relationship("New",
                        secondary=user_news,
                        back_populates="archived_by")

    new_likes = relationship("New",
                             secondary=new_likes,
                             back_populates="likes")

    source_follows = relationship("Source",
                                  secondary=source_follows,
                                  back_populates="follows")
