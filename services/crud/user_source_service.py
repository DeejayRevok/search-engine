"""User source entity operations service"""
from models import UserSource
from services.crud.crud_service import CRUDService


class UserSourceService(CRUDService):
    """User source service implementation class"""

    entity_class = UserSource
