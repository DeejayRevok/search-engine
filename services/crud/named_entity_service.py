"""NamedEntity entity operations service"""
from models.named_entity import NamedEntity
from services.crud.crud_service import CRUDService


class NamedEntityService(CRUDService):
    """NamedEntity entity service implementation class"""

    entity_class = NamedEntity
