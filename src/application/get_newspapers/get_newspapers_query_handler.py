from logging import Logger

from bus_station.query_terminal.query_handler import QueryHandler
from bus_station.query_terminal.query_response import QueryResponse

from application.get_newspapers.get_newspapers_query import GetNewspapersQuery
from domain.newspaper.find_newspaper_criteria import FindNewspaperCriteria
from domain.newspaper.newspaper_repository import NewspaperRepository


class GetNewspapersQueryHandler(QueryHandler):
    def __init__(self, newspaper_repository: NewspaperRepository, logger: Logger):
        self.__newspaper_repository = newspaper_repository
        self.__logger = logger

    def handle(self, query: GetNewspapersQuery) -> QueryResponse:
        self.__logger.info("Starting getting newspapers")
        newspapers = self.__newspaper_repository.find_by_criteria(FindNewspaperCriteria(user_email=query.user_email))
        self.__logger.info("Finished getting newspapers")
        return QueryResponse(data=list(newspapers))

    @classmethod
    def bus_stop_name(cls) -> str:
        return "query_handler.search_engine.get_newspapers"
