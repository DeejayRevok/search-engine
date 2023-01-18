from __future__ import annotations

from bus_station.command_terminal.bus.command_bus import CommandBus
from graphene import Mutation, Boolean, UUID
from pypendency.builder import container_builder

from application.delete_newspaper.delete_newspaper_command import DeleteNewspaperCommand
from infrastructure.graphql.decorators.login_required import login_required


class DeleteNewspaperMutation(Mutation):
    success = Boolean(description="True if the mutation was applied successfully, False otherwise")

    class Arguments:
        id = UUID(required=True, description="Id of the newspaper to delete")

    @staticmethod
    @login_required
    async def mutate(_, __, id: UUID) -> DeleteNewspaperMutation:
        command_bus: CommandBus = container_builder.get(
            "bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus"
        )

        command_bus.transport(DeleteNewspaperCommand(
            newspaper_id=str(id)
        ))

        return DeleteNewspaperMutation(success=True)
