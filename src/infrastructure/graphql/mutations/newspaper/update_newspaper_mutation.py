from __future__ import annotations
from typing import List as TypingList

from bus_station.command_terminal.bus.command_bus import CommandBus
from graphene import Mutation, String, List, Boolean
from graphql import GraphQLResolveInfo
from pypendency.builder import container_builder

from application.update_newspaper.update_newspaper_command import UpdateNewspaperCommand
from infrastructure.graphql.decorators.login_required import login_required


class UpdateNewspaperMutation(Mutation):
    success = Boolean(description="True if the mutation was applied successfully, False otherwise")

    class Arguments:
        original_name = String(required=True, description="Newspaper original name")
        new_name = String(required=False, description="Newspaper new name")
        new_named_entities = List(String, required=False, description="Newspaper new named entities")

    @staticmethod
    @login_required
    async def mutate(
        _,
        info: GraphQLResolveInfo,
        original_name: str,
        new_name: str = None,
        new_named_entities: TypingList[str] = None,
    ) -> UpdateNewspaperMutation:
        user_email: str = info.context["request"].user["email"]

        command_bus: CommandBus = container_builder.get(
            "bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus"
        )

        command_bus.transport(UpdateNewspaperCommand(
            original_name=original_name,
            new_name=new_name,
            user_email=user_email,
            new_named_entities_values=new_named_entities
        ))

        return UpdateNewspaperMutation(success=True)
