"""User new entity operations service"""
from models import UserNew
from services.crud.crud_service import CRUDService


class UserNewService(CRUDService):
    """User new service implementation class"""

    entity_class = UserNew
