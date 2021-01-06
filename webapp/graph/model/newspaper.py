"""
Newspaper models GraphQL module
"""
from typing import List

from graphene import Node, List as GraphList
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphql import ResolveInfo

from news_service_lib.graphql import login_required

from models import Newspaper as NewspaperModel, NamedEntity as NamedEntityModel, NounChunk as NounChunkModel
from webapp.graph.model import NewSchema
from webapp.graph.model.news_search import SearchOperation, SearchField, TrackInfo, SearchTracker


class Newspaper(SQLAlchemyObjectType):
    """
    GraphQL newspaper model schema
    """
    class Meta:
        """
        Newspaper schema metadata
        """
        model = NewspaperModel
        interfaces = (Node,)
        exclude_fields = ('user_id',)

    news: List[NewSchema] = GraphList(NewSchema, description="Newspaper news")

    @staticmethod
    @login_required
    async def resolve_news(root, info: ResolveInfo):
        """
        Get the newspaper news
        Args:
            root: GraphQL base schema model
            info: resolving info

        Returns: newspaper search news

        """
        previous_track_info = None
        named_entities: List[NamedEntityModel] = list(root.named_entities)
        noun_chunks: List[NounChunkModel] = list(root.noun_chunks)
        if len(named_entities):
            previous_track_info = TrackInfo(operation=SearchOperation.UNION,
                                            field=SearchField.NAMED_ENTITY,
                                            value=named_entities.pop(0).value,
                                            previous_track=None)
        elif len(noun_chunks):
            previous_track_info = TrackInfo(operation=SearchOperation.UNION,
                                            field=SearchField.NOUN_CHUNK,
                                            value=noun_chunks.pop(0).value,
                                            previous_track=None)

        if previous_track_info:

            for named_entity in named_entities:
                track = TrackInfo(operation=SearchOperation.INTERSECTION,
                                  field=SearchField.NAMED_ENTITY,
                                  value=named_entity.value,
                                  previous_track=previous_track_info)
                previous_track_info = track

            for noun_chunk in noun_chunks:
                track = TrackInfo(operation=SearchOperation.INTERSECTION,
                                  field=SearchField.NOUN_CHUNK,
                                  value=noun_chunk.value,
                                  previous_track=previous_track_info)
                previous_track_info = track

            return list(SearchTracker.tracking_query(previous_track_info, NewSchema.get_query(info)))
        else:
            return list()


class NewspaperFilter(FilterSet):
    """
    GraphQL newspaper filters schema
    """
    class Meta:
        """
        Newspaper filter schema metadata
        """
        model = NewspaperModel
        fields = {
            'name': [...]
        }
