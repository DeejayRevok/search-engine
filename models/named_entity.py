"""
Named entity database model definition module
"""
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from models.base import BASE
from models.named_entity_type import NamedEntityType
from models.newspaper import named_entities_association

news_association = Table('new_named_entity', BASE.metadata,
                         Column('new_id', Integer, ForeignKey('new.id')),
                         Column('named_entity_id', Integer, ForeignKey('named_entity.id')))


class NamedEntity(BASE):
    """
    Named entity model
    """
    __tablename__ = 'named_entity'

    id = Column(Integer, primary_key=True)
    value = Column(String(255), unique=True)
    named_entity_type_id = Column(Integer, ForeignKey('named_entity_type.id'), nullable=False)

    named_entity_type: NamedEntityType = relationship('NamedEntityType',
                                                      lazy='select',
                                                      uselist=False,
                                                      backref=backref('named_entities', lazy='select'))
    news = relationship(
        "New",
        secondary=news_association,
        back_populates="named_entities")

    newspapers = relationship(
        "Newspaper",
        secondary=named_entities_association,
        back_populates="named_entities")

    def __iter__(self) -> iter:
        """
        Iterate over the model properties

        Returns: iterator to the model properties

        """
        yield 'value', self.value
        yield 'named_entity_type', dict(self.named_entity_type)
