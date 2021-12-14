from logging import Logger

import asyncio
import platform
import sys
from multiprocessing import Process
import json
from sqlalchemy.engine import Engine
from typing import List

from dacite import from_dict

from infrastructure.repositories.named_entity_repository import NamedEntityRepository
from infrastructure.repositories.named_entity_type_repository import NamedEntityTypeRepository
from infrastructure.repositories.new_repository import NewRepository
from infrastructure.repositories.noun_chunk_repository import NounChunkRepository
from infrastructure.repositories.source_repository import SourceRepository
from models.named_entity_type import NamedEntityType
from models.named_entity import NamedEntity as NamedEntityModel
from models.new import New as NewModel
from models.noun_chunk import NounChunk
from models.source import Source
from news_service_lib.messaging.exchange_consumer import ExchangeConsumer

from config import config
from news_service_lib.models.named_entity import NamedEntity
from news_service_lib.models.new import New
from news_service_lib.storage.sql.session_provider import SqlSessionProvider
from webapp.container_config import container


class IndexService:
    def __init__(self, logger: Logger, sql_storage_engine: Engine):
        self.__logger = logger
        self.__logger.info("Starting indexing service")
        self.__session_provider = SqlSessionProvider(sql_storage_engine)
        self.__source_repository = SourceRepository(self.__session_provider, self.__logger)
        self.__new_repository = NewRepository(self.__session_provider, self.__logger)
        self.__named_entity_repository = NamedEntityRepository(self.__session_provider, self.__logger)
        self.__named_entity_type_repository = NamedEntityTypeRepository(self.__session_provider, self.__logger)
        self.__noun_chunk_repository = NounChunkRepository(self.__session_provider, self.__logger)

        self.__exchange_consumer = ExchangeConsumer(
            **config.rabbit,
            exchange="news",
            queue_name="news-indexing",
            message_callback=self.index_message,
            logger=self.__logger,
        )

        if not self.__exchange_consumer.test_connection():
            self.__logger.error("Error connecting to the queue provider. Exiting...")
            sys.exit(1)

        self.__consume_process = None
        if platform.system() != "Windows":
            self.__logger.info("Starting consumer process")
            self.__consume_process = Process(target=self.__exchange_consumer.__call__)
            self.__consume_process.start()

    async def __index_source(self, source_name: str) -> Source:
        saved_source: Source = await self.__source_repository.get_one_filtered(name=source_name)
        if saved_source is None:
            saved_source = await self.__source_repository.save(Source(name=source_name))
        return saved_source

    async def __index_new(self, new_title: str, new_url: str, new_sentiment: float, source: Source) -> NewModel:
        saved_new: NewModel = await self.__new_repository.get_one_filtered(title=new_title)
        if saved_new is None:
            saved_new = await self.__new_repository.save(
                NewModel(title=new_title, url=new_url, sentiment=new_sentiment, source_id=source.id)
            )
        elif saved_new is not None and saved_new.sentiment != new_sentiment:
            saved_new.sentiment = new_sentiment
            saved_new = await self.__new_repository.save(saved_new)
        return saved_new

    async def __index_named_entities(self, named_entities: List[NamedEntity], entities_saved_new: NewModel):
        async def __index_named_entity_type(name: str, description: str = None) -> NamedEntityType:
            saved_named_entity_type: NamedEntityType = await self.__named_entity_type_repository.get_one_filtered(
                name=name
            )
            if saved_named_entity_type is None:
                saved_named_entity_type = await self.__named_entity_type_repository.save(
                    NamedEntityType(name=name, description=description)
                )
            return saved_named_entity_type

        async def __index_named_entity(
            value: str, named_entity_type: NamedEntityType, new_model: NewModel
        ) -> NamedEntityModel:
            saved_named_entity: NamedEntityModel = await self.__named_entity_repository.get_one_filtered(value=value)
            if saved_named_entity is None:
                saved_named_entity = await self.__named_entity_repository.save(
                    NamedEntityModel(value=value, named_entity_type_id=named_entity_type.id)
                )
            saved_named_entity.news.append(new_model)
            return saved_named_entity

        for named_entity in named_entities:
            try:
                named_ent_type = await __index_named_entity_type(named_entity.type)
                await __index_named_entity(named_entity.text, named_ent_type, entities_saved_new)
            except Exception as ex:
                self.__logger.error(
                    "Error while indexing named entity %s: %s", named_entity.text, str(ex), exc_info=True
                )

    async def __index_noun_chunks(self, noun_chunks: List[str], chunks_saved_new: NewModel):
        async def __index_noun_chunk(value: str, new_model: NewModel) -> NounChunk:
            saved_noun_chunk: NounChunk = await self.__noun_chunk_repository.get_one_filtered(value=value)
            if saved_noun_chunk is None:
                saved_noun_chunk = await self.__noun_chunk_repository.save(NounChunk(value=value))
            saved_noun_chunk.news.append(new_model)
            return saved_noun_chunk

        for noun_chunk in noun_chunks:
            try:
                await __index_noun_chunk(noun_chunk, chunks_saved_new)
            except Exception as ex:
                self.__logger.error("Error while indexing noun chunk %s: %s", noun_chunk, str(ex), exc_info=True)

    async def index_new(self, new: New) -> NewModel:
        with self.__session_provider(read_only=False):
            if new.source is not None:
                saved_source_model = await self.__index_source(new.source)

            if new.title is not None:
                saved_new_model = await self.__index_new(new.title, new.url, new.sentiment, saved_source_model)

            if new.entities is not None:
                await self.__index_named_entities(new.entities, saved_new_model)

            if new.noun_chunks is not None:
                await self.__index_noun_chunks(new.noun_chunks, saved_new_model)

        return saved_new_model

    def index_message(self, _, __, ___, body: str):
        apm = container.get("apm")
        apm.begin_transaction("consume")
        try:
            body = json.loads(body)
            self.__logger.info("Indexing new %s", body["title"])
            new = from_dict(New, body)
            asyncio.run(self.index_new(new))

            apm.end_transaction("New index", "OK")
        except Exception as ex:
            self.__logger.error("Error while indexing new %s", str(ex), exc_info=True)
            apm.end_transaction("New index", "FAIL")
            apm.capture_exception()

    async def shutdown(self):
        self.__logger.info("Shutting down indexing service")
        self.__exchange_consumer.shutdown()
        if self.__consume_process:
            self.__consume_process.join()
