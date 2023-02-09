from dataclasses import asdict
from typing import List as TypingList, Optional

from bus_station.query_terminal.bus.query_bus import QueryBus
from graphene import ObjectType, Field, List, String
from pypendency.builder import container_builder

from application.get_newspapers.get_newspapers_query import GetNewspapersQuery
from infrastructure.graphql.decorators.login_required import login_required
from infrastructure.graphql.models.newspaper import Newspaper


class NewspaperQueries(ObjectType):
    newspapers = Field(List(Newspaper), user_email=String(), description="Find newspapers")

    @staticmethod
    @login_required
    async def resolve_newspapers(_, __, user_email: Optional[str] = None) -> TypingList[dict]:
        query_bus: QueryBus = container_builder.get(
            "bus_station.query_terminal.bus.synchronous.sync_query_bus.SyncQueryBus"
        )
        query = GetNewspapersQuery(user_email=user_email)
        return [asdict(newspaper) for newspaper in query_bus.transport(query).data]
