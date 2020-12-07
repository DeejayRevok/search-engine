"""NounChunk entity operations service"""
from models.noun_chunk import NounChunk
from services.crud.crud_service import CRUDService


class NounChunkService(CRUDService):
    """NounChunk service implementation class"""

    entity_class = NounChunk
