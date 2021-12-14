from unittest import TestCase

from models.base import BASE
from models.new import New
from news_service_lib.storage.sql.engine_type import SqlEngineType
from news_service_lib.storage.sql.session_provider import SqlSessionProvider
from news_service_lib.storage.sql.utils import create_sql_engine
from webapp.graph.model.news_search import TrackInfo, SearchOperation, SearchField, SearchTracker


class TestNewsSearch(TestCase):
    def setUp(self) -> None:
        test_engine = create_sql_engine(SqlEngineType.SQLITE)
        self.session_provider = SqlSessionProvider(test_engine)
        BASE.query = self.session_provider.query_property
        BASE.metadata.bind = test_engine
        BASE.metadata.create_all()

    def test_searchable_tracking_query(self):
        first_track_info = TrackInfo(
            operation=SearchOperation.UNION, field=SearchField.NAMED_ENTITY, value="test_first", previous_track=None
        )
        second_track_info = TrackInfo(
            operation=SearchOperation.INTERSECTION,
            field=SearchField.NOUN_CHUNK,
            value="test_second",
            previous_track=first_track_info,
        )
        third_track_info = TrackInfo(
            operation=SearchOperation.INTERSECTION,
            field=SearchField.NOUN_CHUNK,
            value="test_third",
            previous_track=second_track_info,
        )
        fourth_track_info = TrackInfo(
            operation=SearchOperation.UNION,
            field=SearchField.NAMED_ENTITY,
            value="test_fourth",
            previous_track=third_track_info,
        )

        self.assertEqual(first_track_info.next, second_track_info)
        self.assertEqual(second_track_info.next, third_track_info)
        self.assertEqual(third_track_info.next, fourth_track_info)

        full_tracking_query = SearchTracker.tracking_query(third_track_info, New.query)
        self.assertIsNotNone(full_tracking_query)
        self.assertTrue(str(full_tracking_query).count("JOIN noun_chunk"), 2)
        self.assertIn("UNION", str(full_tracking_query))
