import os

from pypendency.builder import container_builder
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session


def load() -> None:
    container_builder.set("sqlalchemy.MetaData", MetaData())
    database_engine = __create_database_engine()
    container_builder.set("sqlalchemy.engine.Engine", database_engine)
    container_builder.set("sqlalchemy.orm.session.Session", __create_database_session(database_engine))

    container_builder.get(
        "infrastructure.database.mappers.sqlalchemy_named_entity_type_mapper.SQLAlchemyNamedEntityTypeMapper"
    ).map()
    container_builder.get(
        "infrastructure.database.mappers.sqlalchemy_named_entity_mapper.SQLAlchemyNamedEntityMapper"
    ).map()
    container_builder.get("infrastructure.database.mappers.sqlalchemy_source_mapper.SQLAlchemySourceMapper").map()
    container_builder.get("infrastructure.database.mappers.sqlalchemy_user_mapper.SQLAlchemyUserMapper").map()
    container_builder.get("infrastructure.database.mappers.sqlalchemy_new_mapper.SQLAlchemyNewMapper").map()
    container_builder.get("infrastructure.database.mappers.sqlalchemy_newspaper_mapper.SQLAlchemyNewspaperMapper").map()


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
