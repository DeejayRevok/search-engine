from typing import List

from graphene import Node, List as GraphList
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphql import ResolveInfo

from news_service_lib.graph.graphql_utils import login_required

from models.newspaper import Newspaper as NewspaperModel
from models.named_entity import NamedEntity as NamedEntityModel
from models.noun_chunk import NounChunk as NounChunkModel
from webapp.graph.model.new_schema import NewSchema
from webapp.graph.model.news_search.track_info import TrackInfo
from webapp.graph.model.news_search.search_operation import SearchOperation
from webapp.graph.model.news_search.search_field import SearchField
from webapp.graph.model.news_search.search_tracker_interface import SearchTracker


class Newspaper(SQLAlchemyObjectType):
    class Meta:
        model = NewspaperModel
        interfaces = (Node,)
        exclude_fields = ('user_id',)

    news: List[NewSchema] = GraphList(NewSchema, description="Newspaper news")

    @staticmethod
    @login_required
    async def resolve_news(root, info: ResolveInfo):
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
    class Meta:
        model = NewspaperModel
        fields = {
            'name': [...]
        }
