from dataclasses import asdict
from typing import List as TypingList, Optional

from bus_station.query_terminal.bus.synchronous.sync_query_bus import SyncQueryBus
from graphene import ObjectType, Field, List, String, UUID, Enum, Argument
from yandil.container import default_container

from application.get_new.get_new_query import GetNewQuery
from application.get_news.get_news_query import GetNewsQuery
from domain.new.sort_news_criteria import SortNewsCriteria
from infrastructure.graphql.decorators.login_required import login_required
from infrastructure.graphql.models.new import New


class NewQueries(ObjectType):
    news = Field(
        List(New),
        title=String(required=False),
        source=String(required=False),
        sort_criteria=Argument(Enum.from_enum(SortNewsCriteria)),
        description="Find news filtered",
    )
    news_by_named_entities_union = Field(
        List(New),
        named_entities=List(String),
        description="Find news which are associated to at least one named entity from a list",
    )
    new = Field(New, id=UUID(), description="Find a specific new")

    @staticmethod
    @login_required
    async def resolve_news_by_named_entities_union(_, __, named_entities: TypingList[str]) -> TypingList[dict]:
        query_bus = default_container[SyncQueryBus]
        query = GetNewsQuery(any_named_entity=named_entities)
        return [asdict(new) for new in query_bus.transport(query).data]

    @staticmethod
    @login_required
    async def resolve_news(
        _,
        __,
        title: Optional[str] = None,
        source: Optional[str] = None,
        sort_criteria: Optional[SortNewsCriteria] = None,
    ) -> TypingList[dict]:
        query_bus = default_container[SyncQueryBus]
        query = GetNewsQuery(
            title=title, source=source, sorting=sort_criteria.value if sort_criteria is not None else None
        )
        return [asdict(new) for new in query_bus.transport(query).data]

    @staticmethod
    @login_required
    async def resolve_new(_, __, id: UUID) -> Optional[dict]:
        query_bus = default_container[SyncQueryBus]
        query = GetNewQuery(id=str(id))
        new = query_bus.transport(query).data
        return asdict(new) if new is not None else None
