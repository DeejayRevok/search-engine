"""
CRUD service module
"""
from typing import Iterator, List, Any

from news_service_lib.storage import StorageError, storage_factory, StorageType
from news_service_lib.storage.filter import Filter, MatchFilter
from news_service_lib.storage.implementation import Storage
from news_service_lib.storage.sql import SqlSessionProvider

from log_config import get_logger
from models import BASE

LOGGER = get_logger()


class CRUDService:
    """
    CRUD service base class implementation
    """
    entity_class: BASE = None

    def __init__(self, session_provider: SqlSessionProvider):
        """
        Initialize the CRUD service for an specific entity

        Args:
            session_provider: SQL sessions provider
        """

        self._repo: Storage = storage_factory(StorageType.SQL.value,
                                              dict(session_provider=session_provider, model=self.entity_class),
                                              logger=LOGGER)

    async def save(self, **properties) -> BASE:
        """
        Save a new instance of this service entity class with the given properties

        Args:
            properties: properties of the instance to save

        Returns: created instance

        """
        try:
            return self._repo.save(self.entity_class(**properties))
        except StorageError as sterr:
            raise ValueError(f'Error saving with properties {properties}') from sterr

    async def update(self, entity: BASE, **update_properties) -> BASE:
        """
        Update the given entity with the specified properties

        Args:
            entity: entity to update
            **update_properties: properties to set to the entity

        Returns: updated entity

        """
        if update_properties:
            for property_key, property_value in update_properties.items():
                if hasattr(entity, property_key):
                    setattr(entity, property_key, property_value)
                else:
                    raise ValueError(f'{entity.__class__.__name__} has no property {property_key}')
            try:
                return self._repo.save(entity)
            except StorageError as sterr:
                raise ValueError(f'Error updating with properties {update_properties}') from sterr

    @staticmethod
    async def _parse_filters(**filters) -> List[Filter]:
        """
        Parse the input filters into a readable format for the repo interface

        Args:
            filters: filters to parse (filter_name=filter_value)

        Returns: parsed filters

        """
        filters_parsed = list()
        for filter_key, filter_val in filters.items():
            filters_parsed.append(MatchFilter(filter_key, filter_val))
        return filters_parsed

    async def read_all(self, **filters) -> Iterator[BASE]:
        """
        Get all the entities which match the given filters

        Args:
            filters: filters to apply to the query

        Returns: entities which matches the given filters

        """
        filters = await self._parse_filters(**filters)
        return self._repo.get(filters)

    async def read_one(self, **filters) -> BASE:
        """
        Get one entity which matches the given filters

        Args:
            filters: filters to apply

        Returns: filters matching query

        """
        filters = await self._parse_filters(**filters)
        return self._repo.get_one(filters)

    async def delete(self, identifier: Any):
        """
        Delete the entity identified by the given identifier

        Args:
            identifier: identifier of the entity to delete

        """
        self._repo.delete(identifier)
