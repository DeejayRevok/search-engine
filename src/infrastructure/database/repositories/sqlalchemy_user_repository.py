from sqlalchemy.orm import Session

from domain.user.user import User
from domain.user.user_repository import UserRepository


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.__sqlalchemy_session = session

    def save(self, user: User) -> None:
        self.__sqlalchemy_session.merge(user)
        self.__sqlalchemy_session.commit()
