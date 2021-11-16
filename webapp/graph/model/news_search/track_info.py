from __future__ import annotations
from typing import Any, Optional

from graphene import String, ObjectType
from sqlalchemy.orm import Query

from webapp.graph.model.news_search import SearchOperation, SearchField


class TrackInfo(ObjectType):
    operation = String()
    field = String()
    value = String()

    def __init__(self, operation: SearchOperation, field: SearchField, value: Any, previous_track: Optional[TrackInfo],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous = previous_track
        self.operation = operation
        self.field = field
        self.value = value
        self.next: Optional[TrackInfo] = None
        if self.previous:
            self.previous.next = self

    def forward_query(self, base_query: Query, aggregated_query: Optional[Query]) -> Query:
        self_aggregated_query = self.field.query(base_query, self.value)
        if aggregated_query is not None:
            self_aggregated_query = self.operation.query(self_aggregated_query, aggregated_query)

        if self.next:
            return self.next.forward_query(base_query, self_aggregated_query)
        else:
            return self_aggregated_query
