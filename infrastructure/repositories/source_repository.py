from infrastructure.repositories.crud_repository import CRUDRepository
from models.source import Source


class SourceRepository(CRUDRepository):
    _ENTITY_CLASS = Source
