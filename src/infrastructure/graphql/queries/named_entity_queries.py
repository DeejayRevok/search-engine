from dataclasses import asdict
from typing import List as TypingList

from graphene import ObjectType, Field, List
from yandil.container import default_container

from application.get_named_entities.get_named_entities_query import GetNamedEntitiesQuery
from infrastructure.graphql.decorators.login_required import login_required
from infrastructure.graphql.models.named_entity import NamedEntity


class NamedEntityQueries(ObjectType):
    named_entities = Field(List(NamedEntity), description="Find named entities")

    @staticmethod
    @login_required
    async def resolve_named_entities(_, __) -> TypingList[dict]:
        query_bus = default_container.get("bus_station.query_terminal.bus.synchronous.sync_query_bus.SyncQueryBus")
        query = GetNamedEntitiesQuery()
        return [asdict(named_entity) for named_entity in query_bus.transport(query).data]
