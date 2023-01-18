from bus_station.query_terminal.bus.query_bus import QueryBus
from graphene import ObjectType, Float, String, List, Field, UUID
from pypendency.builder import container_builder

from infrastructure.graphql.models.named_entity import NamedEntity
from infrastructure.graphql.models.new_detail import NewDetail
from infrastructure.graphql.models.source import Source
from infrastructure.news_manager.get_new_query import GetNewQuery


class New(ObjectType):
    id = UUID(description="New id")
    title = String(description="New title")
    url = String(description="New html url")
    source = Field(Source)
    named_entities = List(NamedEntity, description="New named entities")
    sentiment = Float(description="New sentiment intensity")
    detail = Field(NewDetail, description="New detailed information")

    @staticmethod
    async def resolve_detail(root: dict, _) -> dict:
        query_bus: QueryBus = container_builder.get(
            "bus_station.query_terminal.bus.synchronous.distributed.rpyc_query_bus.RPyCQueryBus"
        )
        query = GetNewQuery(
            title=root["title"]
        )
        query_response = query_bus.transport(query)
        return {
            "content": query_response.data["content"],
            "date": query_response.data["date"],
            "hydrated": query_response.data["hydrated"],
            "summary": query_response.data["summary"]
        }
