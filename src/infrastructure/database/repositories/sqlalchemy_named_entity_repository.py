from typing import List

from sqlalchemy.orm import Session, Query

from domain.named_entity.find_named_entities_criteria import FindNamedEntitiesCriteria
from domain.named_entity.named_entity import NamedEntity

from domain.named_entity.named_entity_repository import NamedEntityRepository


class SQLAlchemyNamedEntityRepository(NamedEntityRepository):

    def __init__(self, sqlalchemy_session: Session):
        self.__sqlalchemy_session = sqlalchemy_session

    def find_by_criteria(self, criteria: FindNamedEntitiesCriteria) -> List[NamedEntity]:
        query = self.__sqlalchemy_session.query(NamedEntity)

        if criteria.value_in is not None:
            query = query.filter(NamedEntity.value.in_(criteria.value_in))

        return query.all()
