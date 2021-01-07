"""
Newspapers mutations module
"""
from typing import List, Union, Optional

from graphene import Mutation, String, List as GraphList, Boolean, ObjectType
from graphql import ResolveInfo
from news_service_lib.graphql import login_required
from news_service_lib.storage.sql import SqlSessionProvider

from log_config import get_logger
from models import Newspaper as NewspaperModel, NamedEntity as NamedEntityModel, NounChunk as NounChunkModel
from services.crud.crud_service import CRUDService
from services.crud.named_entity_service import NamedEntityService
from services.crud.newspaper_service import NewspaperService
from services.crud.noun_chunk_service import NounChunkService

LOGGER = get_logger()


async def _associate(association_service: CRUDService, association_value: str, newspaper: NewspaperModel):
    """
    Associate newspaper with the association value using the association service

    Args:
        association_service: service used to associate
        association_value: value to associate with the newspaper
        newspaper: newspaper to associate with the value

    """
    association_entity: Union[NamedEntityModel, NounChunkModel] = await association_service.read_one(
        value=association_value)
    if association_entity:
        association_entity.newspapers.append(newspaper)
    else:
        LOGGER.warning('Association entity %s not found', association_value)


class CreateNewspaper(Mutation):
    """
    Mutation to create a newspaper
    """
    name = String(description="Name of the created newspaper")

    class Arguments:
        """
        Mutation arguments
        """
        name = String(required=True, description='Newspaper name')
        named_entities = GraphList(String, required=False, description="Newspaper search named entities")
        noun_chunks = GraphList(String, required=False, description="Newspaper search noun chunks")

    @staticmethod
    @login_required
    async def mutate(_, info, name: str, named_entities: List[str] = None, noun_chunks: List[str] = None):
        """
        Mutation handler which creates the newspaper with the provided data

        Args:
            info: mutation resolving info
            name: newspaper name
            named_entities: newspaper named entities
            noun_chunks: nespaper noun chunks

        Returns: create mutation

        """
        user_id: int = info.context['request'].user['id']

        session_provider: SqlSessionProvider = info.context['request'].app['session_provider']
        newspaper_service: NewspaperService = info.context['request'].app['newspaper_service']

        with session_provider(read_only=False):
            newspaper: NewspaperModel = await newspaper_service.save(name=name, user_id=user_id)

            if named_entities:
                named_entity_service: NamedEntityService = info.context['request'].app['named_entity_service']
                for named_entity_val in named_entities:
                    await _associate(named_entity_service, named_entity_val, newspaper)
            if noun_chunks:
                noun_chunks_service: NounChunkService = info.context['request'].app['noun_chunks_service']
                for noun_chunk_val in noun_chunks:
                    await _associate(noun_chunks_service, noun_chunk_val, newspaper)

        return CreateNewspaper(name=newspaper.name)


class UpdateNewspaper(Mutation):
    """
    Mutation to update a newspaper
    """
    name = String(description="Name of the updated newspaper")

    class Arguments:
        """
        Mutation arguments
        """
        original_name = String(required=True, description='Newspaper original name')
        update_name = String(required=False, description='Newspaper updated name')
        named_entities = GraphList(String, required=False, description="Newspaper updated named entities")
        noun_chunks = GraphList(String, required=False, description="Newspaper updated noun chunks")

    @staticmethod
    async def _update_association(info: ResolveInfo, association_entities: Optional[List[str]],
                                  association_service_name: str, newspaper: NewspaperModel, newspaper_assocation: List):
        """
        Update the newspaper association with the input data

        Args:
            info: mutation resolver info
            association_entities: association entities to update
            association_service_name: name of the service to use for the association
            newspaper: newspaper to update
            newspaper_assocation: newspaper association container

        """
        if association_entities is not None:
            association_service: CRUDService = info.context['request'].app[association_service_name]
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
    async def mutate(_, info, original_name: str, update_name: str = None, named_entities: List[str] = None,
                     noun_chunks: List[str] = None):
        """
        Mutation handler

        Args:
            info: resolve information
            original_name: name of the newspaper to update
            update_name: new newspaper name
            named_entities: newspaper new named entities
            noun_chunks: newspaper new noun chunks

        Returns: mutation

        """
        if original_name and (update_name is not None or named_entities is not None or noun_chunks is not None):
            session_provider: SqlSessionProvider = info.context['request'].app['session_provider']
            newspaper_service: NewspaperService = info.context['request'].app['newspaper_service']

            with session_provider(read_only=False):
                newspaper: NewspaperModel = await newspaper_service.read_one(name=original_name)
                if newspaper:
                    if update_name:
                        newspaper.name = update_name

                    await UpdateNewspaper._update_association(info, named_entities, 'named_entity_service', newspaper,
                                                              newspaper.named_entities)

                    await UpdateNewspaper._update_association(info, noun_chunks, 'noun_chunks_service', newspaper,
                                                              newspaper.noun_chunks)
                else:
                    raise ValueError(f'Newspaper {original_name} not found')

            return UpdateNewspaper(name=newspaper.name)
        else:
            return UpdateNewspaper(name=original_name)


class DeleteNewspaper(Mutation):
    """
    Mutation to delete a newspaper
    """
    ok = Boolean()

    class Arguments:
        """
        Mutation arguments
        """
        name = String(required=True, description='Name of the newspaper to delete')

    @staticmethod
    @login_required
    async def mutate(_, info: ResolveInfo, name: str):
        """
        Mutation handler

        Args:
            info: Resolve information
            name: Name of the newspaper to delete

        Returns: mutation

        """
        newspaper_service: NewspaperService = info.context['request'].app['newspaper_service']

        delete_newspaper: NewspaperModel = await newspaper_service.read_one(name=name)
        if delete_newspaper:
            await newspaper_service.delete(delete_newspaper.id)
            return DeleteNewspaper(ok=True)
        else:
            raise ValueError(f'Newspaper {name} not found')


class NewspaperMutations(ObjectType):
    """
    Newspaper GraphQL schema mutations
    """
    create_newspaper = CreateNewspaper.Field()
    update_newspaper = UpdateNewspaper.Field()
    delete_newspaper = DeleteNewspaper.Field()
