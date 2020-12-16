"""
Index Service Module
"""
import asyncio
import sys
from multiprocessing import Process
import json
from typing import List

from aiohttp.web_app import Application

from models import Source, NamedEntityType
from news_service_lib.models import New, NamedEntity
from news_service_lib.messaging.exchange_consumer import ExchangeConsumer

from log_config import get_logger
from services.crud.named_entity_service import NamedEntityService
from services.crud.named_entity_type_service import NamedEntityTypeService
from services.crud.new_service import NewService
from services.crud.source_service import SourceService
from models import New as NewModel
from models import NamedEntity as NamedEntityModel

LOGGER = get_logger()


class IndexService:
    """
    Index service implementation
    """

    def __init__(self, app: Application):
        """
        Initialize the indexing service for the specified app

        Args:
            app: application associated
        """
        LOGGER.info('Starting indexing service')
        self._app = app
        self._exchange_consumer = ExchangeConsumer(**app['config'].get_section('RABBIT'),
                                                   exchange='news',
                                                   queue_name='news-indexing',
                                                   message_callback=self.index_message,
                                                   logger=LOGGER)

        if not self._exchange_consumer.test_connection():
            LOGGER.error('Error connecting to the queue provider. Exiting...')
            sys.exit(1)

        self._consume_process = Process(target=self._exchange_consumer.__call__)
        self._consume_process.start()

    async def _index_source(self, source_name: str) -> Source:
        """
        Index the new data source

        Args:
            source_name: name of the source to index

        Returns: indexed source entity

        """
        source_service: SourceService = self._app['source_service']
        saved_source: Source = await source_service.read_one(name=source_name)
        if not saved_source:
            saved_source = await source_service.save(name=source_name)
        return saved_source

    async def _index_new(self, new_title: str, new_sentiment: float, source: Source) -> NewModel:
        """
        Index the new data

        Args:
            new_title: new title
            new_sentiment: new sentiment score
            source: new indexed source

        Returns: indexed new

        """
        new_service: NewService = self._app['new_service']
        saved_new: NewModel = await new_service.read_one(title=new_title)
        if not saved_new:
            saved_new = await new_service.save(title=new_title, sentiment=new_sentiment, source_id=source.id)
        elif saved_new and saved_new.sentiment != new_sentiment:
            saved_new = await new_service.update(saved_new, sentiment=new_sentiment)
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
            named_entity_type_service: NamedEntityTypeService = self._app['named_entity_type_service']
            saved_named_entity_type: NamedEntityType = await named_entity_type_service.read_one(
                name=name)
            if not saved_named_entity_type:
                saved_named_entity_type = await named_entity_type_service.save(name=name, description=description)
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
            named_entity_service: NamedEntityService = self._app['named_entity_service']
            saved_named_entity: NamedEntityModel = await named_entity_service.read_one(value=value)
            if not saved_named_entity:
                saved_named_entity = await named_entity_service.save(value=value,
                                                                     named_entity_type_id=named_entity_type.id)
            saved_named_entity.news.append(new_model)
            return saved_named_entity

        for named_entity in named_entities:
            named_ent_type = await _index_named_entity_type(named_entity.type)
            await _index_named_entity(named_entity.text, named_ent_type, entities_saved_new)

    async def index_new(self, new: New) -> NewModel:
        """
        Index the input new data with its related entities info into the database

        Args:
            new: new data to index

        Returns: indexed new entity

        """
        with self._app['session_provider'](read_only=False):
            if new.source:
                saved_source_model = await self._index_source(new.source)

            if new.title:
                saved_new_model = await self._index_new(new.title, new.sentiment, saved_source_model)

            if new.entities:
                await self._index_named_entities(new.entities, saved_new_model)

        return saved_new_model

    def index_message(self, _, __, ___, body: str):
        """
        Index the information from the received message

        Args:
            body: message body with the new data

        """
        LOGGER.info('Indexing new')
        self._app['apm'].client.begin_transaction('consume')
        try:
            body = json.loads(body)
            new = New(title=body['title'],
                      content=body['content'],
                      source=body['source'],
                      date=body['date'],
                      hydrated=body['hydrated'],
                      summary=body['summary'],
                      sentiment=body['sentiment'],
                      entities=[NamedEntity(**entity) for entity in body['entities']])

            asyncio.run(self.index_new(new))

            self._app['apm'].client.end_transaction('New index', 'OK')
        except Exception as ex:
            LOGGER.error('Error while indexing new %s', str(ex), exc_info=True)
            self._app['apm'].client.end_transaction('New index', 'FAIL')
            self._app['apm'].client.capture_exception()

    async def shutdown(self):
        """
        Shutdown the indexing service
        """
        LOGGER.info('Shutting down indexing service')
        self._exchange_consumer.shutdown()
        self._consume_process.join()
