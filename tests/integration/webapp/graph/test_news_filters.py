from unittest import TestCase

from aiohttp.web_app import Application
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor
from news_service_lib.storage.sql.engine_type import SqlEngineType
from news_service_lib.storage.sql.session_provider import SqlSessionProvider
from news_service_lib.storage.sql.utils import create_sql_engine

from models.base import BASE
from models.named_entity import NamedEntity
from models.named_entity_type import NamedEntityType
from models.new import New
from models.source import Source
from webapp.container_config import container
from webapp.graph import schema


class MockRequest:
    def __init__(self, user, app):
        self.user = user
        self.app = app


class TestNewsFilters(TestCase):

    BASE_QUERY = """
        query FilterNews($named_entities: [String!]){
                    news(filters: {hasAnyEntity: $named_entities}){
                        edges{
                          node{
                            title
                          }
                        }
                      }
                }
    """

    def setUp(self) -> None:
        container.reset()
        test_engine = create_sql_engine(SqlEngineType.SQLITE)
        self.session_provider = SqlSessionProvider(test_engine)
        BASE.query = self.session_provider.query_property
        BASE.metadata.bind = test_engine
        BASE.metadata.create_all()

        named_entity_type = NamedEntityType(
            id=1, name="Test news filters named entity type", description="Test news filters named entity type"
        )
        self.named_entity_1 = NamedEntity(id=1, named_entity_type=named_entity_type, value="test named entity type 1")
        self.named_entity_2 = NamedEntity(id=2, named_entity_type=named_entity_type, value="test named entity type 2")
        source = Source(id=1, name="Test news filters source")

        self.new_with_entity_1 = New(
            id=1,
            title="Test new with entity 1",
            url="http://test",
            sentiment=1.2,
            source=source,
            named_entities=[self.named_entity_1],
        )
        self.new_with_entity_2 = New(
            id=2,
            title="Test new with entity 2",
            url="http://test",
            sentiment=1.2,
            source=source,
            named_entities=[self.named_entity_2],
        )
        self.new_with_both_entities = New(
            id=3,
            title="Test new with both entities",
            url="http://test",
            sentiment=1.2,
            source=source,
            named_entities=[self.named_entity_1, self.named_entity_2],
        )

        with self.session_provider(read_only=False) as session:
            session.add(self.new_with_entity_1)
            session.add(self.new_with_entity_2)
            session.add(self.new_with_both_entities)

        app = Application()
        self.gql_client = Client(schema)
        self.app = app

    def test_has_any_entity_filter(self):
        scenarios = [
            {
                "msg": "Have entity 1",
                "filter_value": [self.named_entity_1.value],
                "expected_titles": [self.new_with_entity_1.title, self.new_with_both_entities.title],
            },
            {
                "msg": "Have entity 2",
                "filter_value": [self.named_entity_2.value],
                "expected_titles": [self.new_with_entity_2.title, self.new_with_both_entities.title],
            },
            {
                "msg": "Have both entities",
                "filter_value": [self.named_entity_1.value, self.named_entity_2.value],
                "expected_titles": [
                    self.new_with_entity_1.title,
                    self.new_with_entity_2.title,
                    self.new_with_both_entities.title,
                ],
            },
        ]
        for scenario in scenarios:
            with self.subTest(scenario["msg"]):
                query_result = self.gql_client.execute(
                    self.BASE_QUERY,
                    variable_values={"named_entities": scenario["filter_value"]},
                    context_value={"request": MockRequest({"id": 1}, self.app)},
                    executor=AsyncioExecutor(),
                )

                self.assertCountEqual(
                    scenario["expected_titles"], self.__extract_titles_from_query_result(query_result)
                )

    def __extract_titles_from_query_result(self, query_result):
        titles = []
        for node in query_result["data"]["news"]["edges"]:
            titles.append(node["node"]["title"])
        return titles
