from logging import Logger
from uuid import UUID

from bus_station.query_terminal.query_handler import QueryHandler
from bus_station.query_terminal.query_response import QueryResponse

from application.get_new.get_new_query import GetNewQuery
from domain.new.new_repository import NewRepository


class GetNewQueryHandler(QueryHandler):
    def __init__(self, new_repository: NewRepository, logger: Logger):
        self.__new_repository = new_repository
        self.__logger = logger

    def handle(self, query: GetNewQuery) -> QueryResponse:
        self.__logger.info("Starting getting new")
        new = self.__new_repository.find_by_id(UUID(query.id))
        self.__logger.info("Finished getting new")
        return QueryResponse(data=new)

    @classmethod
    def bus_stop_name(cls) -> str:
        return "query_handler.search_engine.get_new"
