from graphene import Interface, Field
from sqlalchemy.orm import Query

from webapp.graph.model.news_search import TrackInfo


class SearchTracker(Interface):
    track_info = Field(TrackInfo)

    @staticmethod
    def tracking_query(last_track_record: TrackInfo, base_query: Query) -> Query:
        track_record = last_track_record
        while track_record.previous is not None:
            track_record = track_record.previous
        return track_record.forward_query(base_query, None)
