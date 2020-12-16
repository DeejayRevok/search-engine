""" New entity operations service"""
from models.new import New
from services.crud.crud_service import CRUDService


class NewService(CRUDService):
    """ New service implementation class"""

    entity_class = New
