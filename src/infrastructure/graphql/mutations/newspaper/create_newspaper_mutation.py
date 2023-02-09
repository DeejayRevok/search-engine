from __future__ import annotations
from typing import List as TypingList

from bus_station.command_terminal.bus.command_bus import CommandBus
from graphene import Mutation, String, List, Boolean
from graphql import GraphQLResolveInfo
from pypendency.builder import container_builder

from application.create_newspaper.create_newspaper_command import CreateNewspaperCommand
from infrastructure.graphql.decorators.login_required import login_required


class CreateNewspaperMutation(Mutation):
    success = Boolean(description="True if the mutation was applied successfully, False otherwise")

    class Arguments:
        name = String(required=True, description="Newspaper name")
        named_entities = List(String, required=True, description="Newspaper named entities")

    @staticmethod
    @login_required
    async def mutate(
        _, info: GraphQLResolveInfo, name: str, named_entities: TypingList[str]
    ) -> CreateNewspaperMutation:
        user_email: str = info.context["request"].user["email"]

        command_bus: CommandBus = container_builder.get(
            "bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus"
        )

        command_bus.transport(
            CreateNewspaperCommand(name=name, user_email=user_email, named_entities_values=named_entities)
        )

        return CreateNewspaperMutation(success=True)
