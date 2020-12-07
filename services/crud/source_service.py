"""Source entity operations service"""
from models.source import Source
from services.crud.crud_service import CRUDService


class SourceService(CRUDService):
    """Source service implementation class"""

    entity_class = Source
