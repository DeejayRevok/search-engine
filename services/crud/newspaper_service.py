"""Newspaper entity operations service"""
from models import Newspaper
from services.crud.crud_service import CRUDService


class NewspaperService(CRUDService):
    """Newspaper service implementation class"""

    entity_class = Newspaper
