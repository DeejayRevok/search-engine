from logging import Logger
from typing import Optional

from bus_station.query_terminal.query_handler import QueryHandler
from bus_station.query_terminal.query_response import QueryResponse

from application.get_news.get_news_query import GetNewsQuery
from domain.new.find_news_criteria import FindNewsCriteria
from domain.new.new_repository import NewRepository
from domain.new.sort_news_criteria import SortNewsCriteria


class GetNewsQueryHandler(QueryHandler):
    def __init__(self, new_repository: NewRepository, logger: Logger):
        self.__new_repository = new_repository
        self.__logger = logger

    def handle(self, query: GetNewsQuery) -> QueryResponse:
        self.__logger.info("Starting getting news")

        find_criteria = self.__get_find_criteria(query)
        sort_criteria = self.__get_sort_criteria(query)
        result = self.__new_repository.find_by_criteria(find_criteria, sort_criteria)

        self.__logger.info("Finished getting news")
        return QueryResponse(
            data=result
        )

    def __get_find_criteria(self, query: GetNewsQuery) -> FindNewsCriteria:
        return FindNewsCriteria(
            title=query.title,
            any_named_entity_value=query.any_named_entity,
            all_named_entities_values=query.all_named_entities,
            source_name=query.source
        )

    def __get_sort_criteria(self, query: GetNewsQuery) -> Optional[SortNewsCriteria]:
        if query.sorting is None:
            return None
        return SortNewsCriteria[query.sorting]

    @classmethod
    def bus_stop_name(cls) -> str:
        return "query_handler.search_engine.get_news"
