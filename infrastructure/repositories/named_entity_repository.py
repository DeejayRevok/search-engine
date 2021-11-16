from infrastructure.repositories.crud_repository import CRUDRepository
from models.named_entity import NamedEntity


class NamedEntityRepository(CRUDRepository):
    _ENTITY_CLASS = NamedEntity
