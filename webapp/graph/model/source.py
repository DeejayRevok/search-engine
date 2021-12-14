from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

from models.source import Source as SourceModel


class Source(SQLAlchemyObjectType):
    class Meta:
        model = SourceModel
        interfaces = (Node,)


class SourceFilter(FilterSet):
    class Meta:
        model = SourceModel
        fields = {"name": [...]}
