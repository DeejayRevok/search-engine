"""
Graphql middlewares module
"""
from typing import Callable

from graphene import ObjectType
from graphql import ResolveInfo

from log_config import get_logger
from news_service_lib.storage.sql import SqlSessionProvider

LOGGER = get_logger()


class SQLMiddleware:
    """
    SQL GraphQL session management enforcement middleware
    """
    def __init__(self, session_provider: SqlSessionProvider):
        """
        Initialize the middleware with the SQL session provider

        Args:
            session_provider: database session provider class
        """
        self._session_provider = session_provider

    def on_error(self, error: Exception):
        """
        Error catching function which clears the database session

        Args:
            error: catched error

        """
        LOGGER.error('Catching error, clearing SQL session')
        self._session_provider.clear_session()
        raise error

    def resolve(self, next_resolver: Callable, root: ObjectType, info: ResolveInfo, **args):
        """
        Resolve the GraphQL clause

        Args:
            next_resolver: next GraphQL resolver
            root: root GraphQL schema
            info: GraphQL resolve context

        Returns: next resolver call

        """
        return next_resolver(root, info, **args).catch(self.on_error)
