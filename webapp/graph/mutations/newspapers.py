from typing import List, Union, Optional

from graphene import Mutation, String, List as GraphList, Boolean, ObjectType

from infrastructure.repositories.crud_repository import CRUDRepository
from infrastructure.repositories.named_entity_repository import NamedEntityRepository
from infrastructure.repositories.newspaper_repository import NewspaperRepository
from infrastructure.repositories.noun_chunk_repository import NounChunkRepository
from news_service_lib.graph.graphql_utils import login_required

from log_config import get_logger
from models.newspaper import Newspaper as NewspaperModel, Newspaper
from models.named_entity import NamedEntity as NamedEntityModel
from models.noun_chunk import NounChunk as NounChunkModel
from news_service_lib.storage.sql.session_provider import SqlSessionProvider
from webapp.container_config import container

LOGGER = get_logger()


async def _associate(association_service: CRUDRepository, association_value: str, newspaper: NewspaperModel):
    association_entity: Union[NamedEntityModel, NounChunkModel] = await association_service.get_one_filtered(
        value=association_value
    )
    if association_entity:
        association_entity.newspapers.append(newspaper)
    else:
        LOGGER.warning("Association entity %s not found", association_value)


class CreateNewspaper(Mutation):
    name = String(description="Name of the created newspaper")

    class Arguments:
        name = String(required=True, description="Newspaper name")
        named_entities = GraphList(String, required=False, description="Newspaper search named entities")
        noun_chunks = GraphList(String, required=False, description="Newspaper search noun chunks")

    @staticmethod
    @login_required
    async def mutate(_, info, name: str, named_entities: List[str] = None, noun_chunks: List[str] = None):
        user_id: int = info.context["request"].user["id"]

        session_provider: SqlSessionProvider = container.get("session_provider")
        newspaper_repository: NewspaperRepository = container.get("newspaper_repository")

        with session_provider(read_only=False):
            newspaper: NewspaperModel = await newspaper_repository.save(Newspaper(name=name, user_id=user_id))

            if named_entities:
                named_entity_repository: NamedEntityRepository = container.get("named_entity_repository")
                for named_entity_val in named_entities:
                    await _associate(named_entity_repository, named_entity_val, newspaper)
            if noun_chunks:
                noun_chunks_repository: NounChunkRepository = container.get("noun_chunk_repository")
                for noun_chunk_val in noun_chunks:
                    await _associate(noun_chunks_repository, noun_chunk_val, newspaper)

        return CreateNewspaper(name=newspaper.name)


class UpdateNewspaper(Mutation):
    name = String(description="Name of the updated newspaper")

    class Arguments:
        original_name = String(required=True, description="Newspaper original name")
        update_name = String(required=False, description="Newspaper updated name")
        named_entities = GraphList(String, required=False, description="Newspaper updated named entities")
        noun_chunks = GraphList(String, required=False, description="Newspaper updated noun chunks")

    @staticmethod
    async def _update_association(
        association_entities: Optional[List[str]],
        association_service: CRUDRepository,
        newspaper: NewspaperModel,
        newspaper_assocation: List,
    ):
        if association_entities is not None:
            delete_associations = list()
            for association in newspaper_assocation:
                if association.value not in association_entities:
                    delete_associations.append(association)
                else:
                    association_entities.remove(association.value)

            for delete_association in delete_associations:
                newspaper_assocation.remove(delete_association)

            for add_association_val in association_entities:
                await _associate(association_service, add_association_val, newspaper)

    @staticmethod
    @login_required
    async def mutate(
        _,
        __,
        original_name: str,
        update_name: str = None,
        named_entities: List[str] = None,
        noun_chunks: List[str] = None,
    ):
        if original_name and (update_name is not None or named_entities is not None or noun_chunks is not None):
            session_provider: SqlSessionProvider = container.get("session_provider")
            newspaper_service: NewspaperRepository = container.get("newspaper_repository")

            with session_provider(read_only=False):
                newspaper: NewspaperModel = await newspaper_service.get_one_filtered(name=original_name)
                if newspaper:
                    if update_name:
                        newspaper.name = update_name

                    named_entity_repository: NamedEntityRepository = container.get("named_entity_repository")
                    await UpdateNewspaper._update_association(
                        named_entities, named_entity_repository, newspaper, newspaper.named_entities
                    )

                    noun_chunks_repository: NounChunkRepository = container.get("noun_chunk_repository")
                    await UpdateNewspaper._update_association(
                        noun_chunks, noun_chunks_repository, newspaper, newspaper.noun_chunks
                    )
                else:
                    raise ValueError(f"Newspaper {original_name} not found")

            return UpdateNewspaper(name=newspaper.name)
        else:
            return UpdateNewspaper(name=original_name)


class DeleteNewspaper(Mutation):
    ok = Boolean()

    class Arguments:
        name = String(required=True, description="Name of the newspaper to delete")

    @staticmethod
    @login_required
    async def mutate(_, __, name: str):
        newspaper_repository: NewspaperRepository = container.get("newspaper_repository")

        delete_newspaper: NewspaperModel = await newspaper_repository.get_one_filtered(name=name)
        if delete_newspaper:
            await newspaper_repository.delete(delete_newspaper)
            return DeleteNewspaper(ok=True)
        else:
            raise ValueError(f"Newspaper {name} not found")


class NewspaperMutations(ObjectType):
    create_newspaper = CreateNewspaper.Field()
    update_newspaper = UpdateNewspaper.Field()
    delete_newspaper = DeleteNewspaper.Field()
