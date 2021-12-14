from typing import Callable

from graphene import ObjectType
from graphql import ResolveInfo

from log_config import get_logger
from news_service_lib.storage.sql.session_provider import SqlSessionProvider

LOGGER = get_logger()


class SQLMiddleware:
    def __init__(self, session_provider: SqlSessionProvider):
        self._session_provider = session_provider

    def on_error(self, error: Exception):
        LOGGER.error("Catching error, clearing SQL session")
        self._session_provider.clear_session()
        raise error

    def resolve(self, next_resolver: Callable, root: ObjectType, info: ResolveInfo, **args):
        return next_resolver(root, info, **args).catch(self.on_error)
