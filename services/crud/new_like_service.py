"""New like entity operations service"""
from models import NewLike
from services.crud.crud_service import CRUDService


class NewLikeService(CRUDService):
    """New like service implementation class"""

    entity_class = NewLike
