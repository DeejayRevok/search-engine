"""
Track info module
"""
from __future__ import annotations
from typing import Any, Optional

from graphene import String, ObjectType
from sqlalchemy.orm import Query

from webapp.graph.model.news_search import SearchOperation, SearchField


class TrackInfo(ObjectType):
    """
    Track info implementation
    """
    operation = String()
    field = String()
    value = String()

    def __init__(self, operation: SearchOperation, field: SearchField, value: Any, previous_track: Optional[TrackInfo],
                 *args, **kwargs):
        """
        Initialize the track info module

        Args:
            operation: search operation
            field: search field
            value: search value
            previous_track: previous track info reference
        """
        super().__init__(*args, **kwargs)
        self.previous = previous_track
        self.operation = operation
        self.field = field
        self.value = value
        self.next: Optional[TrackInfo] = None
        if self.previous:
            self.previous.next = self

    def forward_query(self, base_query: Query, aggregated_query: Optional[Query]) -> Query:
        """
        Get the query equivalent to the current track info following the forward direction

        Args:
            base_query: base query to build the tracking query
            aggregated_query: aggregated query

        Returns: track info forward query

        """
        self_aggregated_query = self.field.query(base_query, self.value)
        if aggregated_query is not None:
            self_aggregated_query = self.operation.query(self_aggregated_query, aggregated_query)

        if self.next:
            return self.next.forward_query(base_query, self_aggregated_query)
        else:
            return self_aggregated_query
