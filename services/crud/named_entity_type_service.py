"""NamedEntity entity operations service"""
from models.named_entity import NamedEntityType
from services.crud.crud_service import CRUDService


class NamedEntityTypeService(CRUDService):
    """NamedEntityType entity service implementation class"""

    entity_class = NamedEntityType
