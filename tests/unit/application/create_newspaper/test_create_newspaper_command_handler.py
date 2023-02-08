from logging import Logger
from unittest import TestCase
from unittest.mock import Mock, patch
from uuid import uuid4

from bus_station.event_terminal.bus.event_bus import EventBus

from application.create_newspaper.create_newspaper_command import CreateNewspaperCommand
from application.create_newspaper.create_newspaper_command_handler import CreateNewspaperCommandHandler
from domain.named_entity.find_named_entities_criteria import FindNamedEntitiesCriteria
from domain.named_entity.named_entity import NamedEntity
from domain.named_entity.named_entity_repository import NamedEntityRepository
from domain.named_entity.named_entity_type import NamedEntityType
from domain.newspaper.newspaper import Newspaper
from domain.newspaper.newspaper_created_event import NewspaperCreatedEvent
from domain.newspaper.newspaper_repository import NewspaperRepository


class TestCreateNewspaperCommandHandler(TestCase):
    def setUp(self) -> None:
        self.newspaper_repository_mock = Mock(spec=NewspaperRepository)
        self.named_entity_repository_mock = Mock(spec=NamedEntityRepository)
        self.event_bus_mock = Mock(spec=EventBus)
        self.logger_mock = Mock(spec=Logger)
        self.command_handler = CreateNewspaperCommandHandler(
            self.newspaper_repository_mock, self.named_entity_repository_mock, self.event_bus_mock, self.logger_mock
        )

    @patch("application.create_newspaper.create_newspaper_command_handler.uuid4")
    def test_handle_success(self, uuid_mock):
        test_uuid = uuid4()
        uuid_mock.return_value = test_uuid
        test_command = CreateNewspaperCommand(
            name="test_newspaper",
            user_email="test_user",
            named_entities_values=["test_named_entity_1", "test_named_entity_2"],
        )
        test_named_entity = NamedEntity(
            value="test_named_entity",
            named_entity_type=NamedEntityType(
                name="test_named_entity_type", description="Test named entity description"
            ),
        )
        self.named_entity_repository_mock.find_by_criteria.return_value = [test_named_entity, test_named_entity]

        self.command_handler.handle(test_command)

        self.named_entity_repository_mock.find_by_criteria.assert_called_once_with(
            FindNamedEntitiesCriteria(value_in=["test_named_entity_1", "test_named_entity_2"])
        )
        self.newspaper_repository_mock.save.assert_called_once_with(
            Newspaper(
                id=test_uuid,
                name="test_newspaper",
                user_email="test_user",
                named_entities=[test_named_entity, test_named_entity],
            )
        )
        expected_event = NewspaperCreatedEvent(
            id=str(test_uuid),
            name="test_newspaper",
            user_email="test_user",
        )
        self.event_bus_mock.transport.assert_called_once_with(expected_event)
