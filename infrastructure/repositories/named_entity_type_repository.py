from infrastructure.repositories.crud_repository import CRUDRepository
from models.named_entity import NamedEntityType


class NamedEntityTypeRepository(CRUDRepository):
    _ENTITY_CLASS = NamedEntityType
