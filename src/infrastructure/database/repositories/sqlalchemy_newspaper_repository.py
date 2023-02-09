from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from domain.newspaper.find_newspaper_criteria import FindNewspaperCriteria
from domain.newspaper.newspaper import Newspaper
from domain.newspaper.newspaper_repository import NewspaperRepository


class SQLAlchemyNewspaperRepository(NewspaperRepository):
    def __init__(self, sqlalchemy_session: Session):
        self.__sqlalchemy_session = sqlalchemy_session

    def save(self, newspaper: Newspaper) -> None:
        self.__sqlalchemy_session.merge(newspaper)
        self.__sqlalchemy_session.commit()

    def find_by_name_and_user_email(self, name: str, user_email: str) -> Optional[Newspaper]:
        return self.__sqlalchemy_session.query(Newspaper).filter_by(name=name, user_email=user_email).one_or_none()

    def find_by_criteria(self, criteria: FindNewspaperCriteria) -> List[Newspaper]:
        query = self.__sqlalchemy_session.query(Newspaper)

        if criteria.user_email is not None:
            query = query.filter_by(user_email=criteria.user_email)

        return query.all()

    def delete(self, newspaper_id: UUID) -> None:
        self.__sqlalchemy_session.query(Newspaper).filter_by(id=newspaper_id).delete()
