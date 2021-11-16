from graphene import Node
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet

from models.noun_chunk import NounChunk as NounChunkModel


class NounChunkSchema(SQLAlchemyObjectType):
    class Meta:
        model = NounChunkModel
        interfaces = (Node,)


class NounChunkFilter(FilterSet):
    class Meta:
        model = NounChunkModel
        fields = {
            'value': [...],
        }
