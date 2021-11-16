from logging import Logger

from sqlalchemy.exc import IntegrityError
from typing import Iterator, Any, ClassVar, Optional

from log_config import get_logger
from models.base import BASE
from news_service_lib.storage.exceptions import StorageIntegrityError, StorageError
from news_service_lib.storage.sql.session_provider import SqlSessionProvider

LOGGER = get_logger()


class CRUDRepository:
    _ENTITY_CLASS: ClassVar[Optional[BASE]] = None

    def __init__(self, sql_session_provider: SqlSessionProvider, logger: Logger):
        self.__session_provider = sql_session_provider
        self.__logger = logger

    async def save(self, entity: BASE) -> BASE:
        try:
            with self.__session_provider(read_only=False) as session:
                session.add(entity)
                return entity
        except IntegrityError as interr:
            self.__logger.error(f"Integrity error trying to save {entity}")
            raise StorageIntegrityError(str(interr)) from interr
        except Exception as ex:
            self.__logger.error(f"Error trying to save {entity}")
            raise StorageError(str(ex))

    async def get_filtered(self, **filters) -> Iterator[BASE]:
        with self.__session_provider() as session:
            return session.query(self._ENTITY_CLASS).filter_by(**filters)

    async def get_one_filtered(self, **filters) -> Optional[BASE]:
        with self.__session_provider() as session:
            return session.query(self._ENTITY_CLASS).filter_by(**filters).one_or_none()

    async def delete(self, entity: BASE) -> None:
        try:
            with self.__session_provider(read_only=False) as session:
                session.query(self._ENTITY_CLASS).filter_by(id=entity.id).delete()
        except Exception as ex:
            self.__logger.error(f"Error while trying to delete {self._ENTITY_CLASS.__class__.__name__}{entity.id}: {str(ex)}")
            raise ex
