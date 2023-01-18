from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

from application.get_named_entities.get_named_entities_query import GetNamedEntitiesQuery
from application.get_named_entities.get_named_entities_query_handler import GetNamedEntitiesQueryHandler
from domain.named_entity.find_named_entities_criteria import FindNamedEntitiesCriteria
from domain.named_entity.named_entity import NamedEntity
from domain.named_entity.named_entity_repository import NamedEntityRepository
from domain.named_entity.named_entity_type import NamedEntityType


class TestGetNamedEntitiesQueryHandler(TestCase):
    def setUp(self) -> None:
        self.named_entity_repository_mock = Mock(spec=NamedEntityRepository)
        self.logger_mock = Mock(spec=Logger)
        self.query_handler = GetNamedEntitiesQueryHandler(
            self.named_entity_repository_mock,
            self.logger_mock
        )

    def test_handle_success(self):
        test_named_entity = NamedEntity(
            value="test_named_entity",
            named_entity_type=NamedEntityType(name="test_named_entity_type", description="Test")
        )
        test_named_entities = [test_named_entity, test_named_entity]
        self.named_entity_repository_mock.find_by_criteria.return_value = test_named_entities
        test_query = GetNamedEntitiesQuery()

        query_response = self.query_handler.handle(test_query)

        self.assertEqual(test_named_entities, query_response.data)
        self.named_entity_repository_mock.find_by_criteria.assert_called_once_with(FindNamedEntitiesCriteria())
