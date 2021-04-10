"""
Index Service Module
"""
import asyncio
import platform
import sys
from multiprocessing import Process
import json
from typing import List

from dacite import from_dict

from news_service_lib.models import New, NamedEntity
from news_service_lib.messaging.exchange_consumer import ExchangeConsumer
from news_service_lib.storage.sql import create_sql_engine, SqlEngineType, SqlSessionProvider

from config import config
from log_config import get_logger
from services.crud.named_entity_service import NamedEntityService
from services.crud.named_entity_type_service import NamedEntityTypeService
from services.crud.new_service import NewService
from services.crud.noun_chunk_service import NounChunkService
from services.crud.source_service import SourceService
from models import Source, NamedEntityType
from models import New as NewModel
from models import NamedEntity as NamedEntityModel
from models import NounChunk as NounChunkModel
from webapp.container_config import container

LOGGER = get_logger()


class IndexService:
    """
    Index service implementation
    """

    def __init__(self):
        """
        Initialize the indexing service
        """
        LOGGER.info('Starting indexing service')
        storage_engine = create_sql_engine(SqlEngineType.MYSQL, **config.storage)
        self._session_provider = SqlSessionProvider(storage_engine)
        self._source_service = SourceService(self._session_provider)
        self._new_service = NewService(self._session_provider)
        self._named_entity_service = NamedEntityService(self._session_provider)
        self._named_entity_type_service = NamedEntityTypeService(self._session_provider)
        self._noun_chunk_service = NounChunkService(self._session_provider)

        self._exchange_consumer = ExchangeConsumer(**config.rabbit,
                                                   exchange='news',
                                                   queue_name='news-indexing',
                                                   message_callback=self.index_message,
                                                   logger=LOGGER)

        if not self._exchange_consumer.test_connection():
            LOGGER.error('Error connecting to the queue provider. Exiting...')
            sys.exit(1)

        self._consume_process = None
        if platform.system() != 'Windows':
            LOGGER.info('Starting consumer process')
            self._consume_process = Process(target=self._exchange_consumer.__call__)
            self._consume_process.start()

    async def _index_source(self, source_name: str) -> Source:
        """
        Index the new data source

        Args:
            source_name: name of the source to index

        Returns: indexed source entity

        """
        saved_source: Source = await self._source_service.read_one(name=source_name)
        if not saved_source:
            saved_source = await self._source_service.save(name=source_name)
        return saved_source

    async def _index_new(self, new_title: str, new_url: str, new_sentiment: float, source: Source) -> NewModel:
        """
        Index the new data

        Args:
            new_title: new title
            new_url: new url
            new_sentiment: new sentiment score
            source: new indexed source

        Returns: indexed new

        """
        saved_new: NewModel = await self._new_service.read_one(title=new_title)
        if not saved_new:
            saved_new = await self._new_service.save(title=new_title, url=new_url, sentiment=new_sentiment,
                                                     source_id=source.id)
        elif saved_new and saved_new.sentiment != new_sentiment:
            saved_new = await self._new_service.update(saved_new, sentiment=new_sentiment)
        return saved_new

    async def _index_named_entities(self, named_entities: List[NamedEntity], entities_saved_new: NewModel):
        """
        Index the named entities into the database

        Args:
            named_entities:  named entities data to index
            entities_saved_new: indexed new where the named entities appear
        """

        async def _index_named_entity_type(name: str, description: str = None) -> NamedEntityType:
            """
            Index the named entity type data

            Args:
                name: named entity type name
                description: named entity type description

            Returns: indexed named entity type

            """
            saved_named_entity_type: NamedEntityType = await self._named_entity_type_service.read_one(name=name)
            if not saved_named_entity_type:
                saved_named_entity_type = await self._named_entity_type_service.save(name=name, description=description)
            return saved_named_entity_type

        async def _index_named_entity(value: str, named_entity_type: NamedEntityType,
                                      new_model: NewModel) -> NamedEntityModel:
            """
            Index the named entity data

            Args:
                value: named entity value
                named_entity_type: named entity indexed type
                new_model: indexed new where the named entity appears

            Returns: indexed named entity

            """
            saved_named_entity: NamedEntityModel = await self._named_entity_service.read_one(value=value)
            if not saved_named_entity:
                saved_named_entity = await self._named_entity_service.save(value=value,
                                                                           named_entity_type_id=named_entity_type.id)
            saved_named_entity.news.append(new_model)
            return saved_named_entity

        for named_entity in named_entities:
            try:
                named_ent_type = await _index_named_entity_type(named_entity.type)
                await _index_named_entity(named_entity.text, named_ent_type, entities_saved_new)
            except Exception as ex:
                LOGGER.error('Error while indexing named entity %s: %s', named_entity.text, str(ex), exc_info=True)

    async def _index_noun_chunks(self, noun_chunks: List[str], chunks_saved_new: NewModel):
        """
        Index the noun chunks into the database

        Args:
            noun_chunks:  noun chunks data to index
            chunks_saved_new: indexed new where the noun chunks appear
        """

        async def _index_noun_chunk(value: str, new_model: NewModel) -> NounChunkModel:
            """
            Index the named entity data

            Args:
                value: noun chunk value
                new_model: indexed new where the noun chunk appears

            Returns: indexed noun chunk

            """
            saved_noun_chunk: NounChunkModel = await self._noun_chunk_service.read_one(value=value)
            if not saved_noun_chunk:
                saved_noun_chunk = await self._noun_chunk_service.save(value=value)
            saved_noun_chunk.news.append(new_model)
            return saved_noun_chunk

        for noun_chunk in noun_chunks:
            try:
                await _index_noun_chunk(noun_chunk, chunks_saved_new)
            except Exception as ex:
                LOGGER.error('Error while indexing noun chunk %s: %s', noun_chunk, str(ex), exc_info=True)

    async def index_new(self, new: New) -> NewModel:
        """
        Index the input new data with its related entities info into the database

        Args:
            new: new data to index

        Returns: indexed new entity

        """
        with self._session_provider(read_only=False):
            if new.source:
                saved_source_model = await self._index_source(new.source)

            if new.title:
                saved_new_model = await self._index_new(new.title, new.url, new.sentiment, saved_source_model)

            if new.entities:
                await self._index_named_entities(new.entities, saved_new_model)

            if new.noun_chunks:
                await self._index_noun_chunks(new.noun_chunks, saved_new_model)

        return saved_new_model

    def index_message(self, _, __, ___, body: str):
        """
        Index the information from the received message

        Args:
            body: message body with the new data

        """
        apm = container.get('apm')
        apm.begin_transaction('consume')
        try:
            body = json.loads(body)
            LOGGER.info('Indexing new %s', body['title'])
            new = from_dict(New, body)
            asyncio.run(self.index_new(new))

            apm.end_transaction('New index', 'OK')
        except Exception as ex:
            LOGGER.error('Error while indexing new %s', str(ex), exc_info=True)
            apm.end_transaction('New index', 'FAIL')
            apm.capture_exception()

    async def shutdown(self):
        """
        Shutdown the indexing service
        """
        LOGGER.info('Shutting down indexing service')
        self._exchange_consumer.shutdown()
        if self._consume_process:
            self._consume_process.join()
