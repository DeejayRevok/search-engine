from logging import Logger

from bus_station.query_terminal.query_handler import QueryHandler
from bus_station.query_terminal.query_response import QueryResponse

from application.get_named_entities.get_named_entities_query import GetNamedEntitiesQuery
from domain.named_entity.find_named_entities_criteria import FindNamedEntitiesCriteria
from domain.named_entity.named_entity_repository import NamedEntityRepository


class GetNamedEntitiesQueryHandler(QueryHandler):
    def __init__(self, named_entity_repository: NamedEntityRepository, logger: Logger):
        self.__named_entity_repository = named_entity_repository
        self.__logger = logger

    def handle(self, query: GetNamedEntitiesQuery) -> QueryResponse:
        self.__logger.info("Starting getting named entities")
        named_entities = self.__named_entity_repository.find_by_criteria(FindNamedEntitiesCriteria())
        self.__logger.info("Finished getting named entities")
        return QueryResponse(data=list(named_entities))

    @classmethod
    def bus_stop_name(cls) -> str:
        return "query_handler.search_engine.get_named_entities"
