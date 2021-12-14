from infrastructure.repositories.crud_repository import CRUDRepository
from models.noun_chunk import NounChunk


class NounChunkRepository(CRUDRepository):
    _ENTITY_CLASS = NounChunk
