from infrastructure.repositories.crud_repository import CRUDRepository
from models.new import New


class NewRepository(CRUDRepository):
    _ENTITY_CLASS = New
