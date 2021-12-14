from infrastructure.repositories.crud_repository import CRUDRepository
from models.user import User


class UserRepository(CRUDRepository):
    _ENTITY_CLASS = User
