from infrastructure.repositories.crud_repository import CRUDRepository
from models.newspaper import Newspaper


class NewspaperRepository(CRUDRepository):
    _ENTITY_CLASS = Newspaper
