from models.user import User
from services.crud.crud_service import CRUDService


class UserService(CRUDService):
    """User service implementation class"""

    entity_class = User
