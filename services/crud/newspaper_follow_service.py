"""Newspaper follow entity operations service"""
from models import NewspaperFollow
from services.crud.crud_service import CRUDService


class NewspaperFollowService(CRUDService):
    """Newspaper follow service implementation class"""

    entity_class = NewspaperFollow
