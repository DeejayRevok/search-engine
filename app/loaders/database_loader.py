import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from yandil.container import default_container

from infrastructure.database.mappers.sqlalchemy_named_entity_mapper import SQLAlchemyNamedEntityMapper
from infrastructure.database.mappers.sqlalchemy_named_entity_type_mapper import SQLAlchemyNamedEntityTypeMapper
from infrastructure.database.mappers.sqlalchemy_new_mapper import SQLAlchemyNewMapper
from infrastructure.database.mappers.sqlalchemy_newspaper_mapper import SQLAlchemyNewspaperMapper
from infrastructure.database.mappers.sqlalchemy_source_mapper import SQLAlchemySourceMapper
from infrastructure.database.mappers.sqlalchemy_user_mapper import SQLAlchemyUserMapper


def load() -> None:
    default_container.add(MetaData)
    database_engine = __create_database_engine()
    default_container[Engine] = database_engine
    default_container[Session] = __create_database_session(database_engine)

    default_container[SQLAlchemyNamedEntityTypeMapper].map()
    default_container[SQLAlchemyNamedEntityMapper].map()
    default_container[SQLAlchemySourceMapper].map()
    default_container[SQLAlchemyUserMapper].map()
    default_container[SQLAlchemyNewMapper].map()
    default_container[SQLAlchemyNewspaperMapper].map()


def __create_database_session(database_engine: Engine) -> Session:
    return scoped_session(session_factory=sessionmaker(bind=database_engine))()


def __create_database_engine() -> Engine:
    db_host = os.environ.get("SEARCH_ENGINE_STORAGE__HOST")
    db_port = os.environ.get("SEARCH_ENGINE_STORAGE__PORT")
    db_user = os.environ.get("SEARCH_ENGINE_STORAGE__USER")
    db_password = os.environ.get("SEARCH_ENGINE_STORAGE__PASSWORD")
    db_name = os.environ.get("SEARCH_ENGINE_STORAGE__DATABASE")
    engine_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(engine_uri)
