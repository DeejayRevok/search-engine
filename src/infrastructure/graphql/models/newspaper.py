from dataclasses import asdict
from typing import List as TypingList

from bus_station.query_terminal.bus.query_bus import QueryBus
from graphene import ObjectType, UUID, String, List
from pypendency.builder import container_builder

from application.get_news.get_news_query import GetNewsQuery
from infrastructure.graphql.models.named_entity import NamedEntity
from infrastructure.graphql.models.new import New


class Newspaper(ObjectType):
    id = UUID(description="Newspaper id")
    name = String(description="Newspaper name")
    user_email = String(description="Newspaper owner email")
    named_entities = List(NamedEntity, description="Newspaper named entities")
    news = List(New, description="Newspaper news")

    @staticmethod
    async def resolve_news(root: dict, _) -> TypingList[dict]:
        query_bus: QueryBus = container_builder.get(
            "bus_station.query_terminal.bus.synchronous.sync_query_bus.SyncQueryBus"
        )
        query = GetNewsQuery(
            any_named_entity=[named_entity["value"] for named_entity in root["named_entities"]]
        )
        return [
            asdict(new) for new in query_bus.transport(query).data
        ]
