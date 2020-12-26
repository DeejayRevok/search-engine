"""
Advanced news search module
"""
from __future__ import annotations
from typing import List

from graphene import ObjectType, List as GraphList, Field, String
from graphql import ResolveInfo
from sqlalchemy.orm import Query

from news_service_lib.graphql import login_required
from webapp.graph.model import NewSchema
from webapp.graph.model.news_search import SearchField, SearchOperation, TrackInfo, SearchTracker


class NewsSearch(ObjectType):
    """
    Advanced news search schema
    """

    class Meta:
        """
        News search schema meta class
        """
        interfaces = (SearchTracker,)

    result: List[NewSchema] = GraphList(NewSchema, description='News searching results')
    union: NewsSearch = Field(lambda: NewsSearch,
                              named_entity=String(required=False),
                              noun_chunk=String(required=False),
                              description="Union search term")
    intersection: NewsSearch = Field(lambda: NewsSearch,
                                     named_entity=String(required=False),
                                     noun_chunk=String(required=False),
                                     description="Intersection search term")

    @staticmethod
    async def search_resolver(operation: SearchOperation, root, info: ResolveInfo, named_entity: str = None,
                              noun_chunk: str = None) -> NewsSearch:
        """
        Resolve the current search transaction using the operation provided

        Args:
            operation: type of operation to perform
            root: root graphql instance
            info: graphql resolve information
            named_entity: named entity filter
            noun_chunk: noun chunk filter

        Returns: searching results

        """
        if not named_entity and not noun_chunk:
            raise ValueError('Input union search filter missing')
        if named_entity and noun_chunk:
            raise ValueError('Multiple input filters')

        query: Query = NewSchema.get_query(info)
        previous_track_info = root.track_info

        aggregated_track_info = None
        if named_entity is not None:
            aggregated_track_info = TrackInfo(operation=operation,
                                              field=SearchField.NAMED_ENTITY,
                                              value=named_entity,
                                              previous_track=previous_track_info)
        elif noun_chunk is not None:
            aggregated_track_info = TrackInfo(operation=operation,
                                              field=SearchField.NOUN_CHUNK,
                                              value=noun_chunk,
                                              previous_track=previous_track_info)

        search_result = NewsSearch(result=list(SearchTracker.tracking_query(aggregated_track_info, query)))
        search_result.track_info = aggregated_track_info
        return search_result

    @staticmethod
    @login_required
    async def resolve_union(root, info: ResolveInfo, named_entity: str = None, noun_chunk: str = None) -> NewsSearch:
        """
        Resolve the union search

        Args:
            root: root graphql instance
            info: graphql resolve information
            named_entity: named entity filter
            noun_chunk: noun chunk filter

        Returns: union search results

        """
        return await NewsSearch.search_resolver(SearchOperation.UNION, root, info, named_entity=named_entity,
                                                noun_chunk=noun_chunk)

    @staticmethod
    @login_required
    async def resolve_intersection(root, info: ResolveInfo, named_entity: str = None,
                                   noun_chunk: str = None) -> NewsSearch:
        """
        Resolve the intersection search

        Args:
            root: root graphql instance
            info: graphql resolve information
            named_entity: named entity filter
            noun_chunk: noun chunk filter

        Returns: intersection search results

        """
        return await NewsSearch.search_resolver(SearchOperation.INTERSECTION, root, info, named_entity=named_entity,
                                                noun_chunk=noun_chunk)
