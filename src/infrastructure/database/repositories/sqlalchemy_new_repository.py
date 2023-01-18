from typing import List, Optional
from uuid import UUID

from sqlalchemy import desc, asc
from sqlalchemy.dialects.postgresql import All
from sqlalchemy.orm import Session, Query

from domain.named_entity.named_entity import NamedEntity
from domain.new.find_news_criteria import FindNewsCriteria
from domain.new.new import New
from domain.new.new_repository import NewRepository
from domain.new.sort_news_criteria import SortNewsCriteria
from domain.source.source import Source


class SQLAlchemyNewRepository(NewRepository):
    def __init__(self, sqlalchemy_session: Session):
        self.__sqlalchemy_session = sqlalchemy_session

    def save(self, new: New) -> None:
        self.__sqlalchemy_session.merge(new)
        self.__sqlalchemy_session.commit()

    def find_by_id(self, new_id: UUID) -> Optional[New]:
        return self.__sqlalchemy_session.query(New).filter_by(id=new_id).one_or_none()

    def find_by_title(self, new_title: str) -> Optional[New]:
        return self.__sqlalchemy_session.query(New).filter_by(title=new_title).one_or_none()

    def find_by_criteria(
            self, criteria: FindNewsCriteria, sort_criteria: Optional[SortNewsCriteria] = None
    ) -> List[New]:
        query = self.__sqlalchemy_session.query(New)
        query = self.__apply_find_criteria(query, criteria)

        if sort_criteria is not None:
            query = self.__apply_sort_criteria(query, sort_criteria)

        return query.all()

    def __apply_find_criteria(self, query: Query, find_criteria: FindNewsCriteria) -> Query:
        if find_criteria.title is not None:
            query = query.filter_by(title=find_criteria.title)

        if find_criteria.any_named_entity_value is not None:
            query = query.join(New.named_entities).filter(NamedEntity.value.in_(find_criteria.any_named_entity_value))

        if find_criteria.all_named_entities_values is not None:
            query = query.join(New.named_entities).filter(All(
                NamedEntity.value,
                find_criteria.all_named_entities_values
            ))

        if find_criteria.source_name is not None:
            query = query.join(New.source).filter(Source.name == find_criteria.source_name)

        return query

    def __apply_sort_criteria(self, query: Query, sort_criteria: SortNewsCriteria) -> Query:
        if sort_criteria == SortNewsCriteria.SENTIMENT_ASCENDANT:
            return query.order_by(asc(New.sentiment))
        if sort_criteria == SortNewsCriteria.SENTIMENT_DESCENDANT:
            return query.order_by(desc(New.sentiment))
        raise NotImplementedError(f"News sort criteria {sort_criteria.value} not supported")
