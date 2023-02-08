from decimal import Decimal
from logging import Logger
from unittest import TestCase
from unittest.mock import Mock, patch
from uuid import uuid4

from bus_station.event_terminal.bus.event_bus import EventBus

from domain.named_entity.named_entity import NamedEntity
from domain.named_entity.named_entity_type import NamedEntityType
from domain.new.indexed_new_event import IndexedNewEvent
from domain.source.source import Source

from domain.new.new import New

from application.index_new.index_new_command import IndexNewCommand
from application.index_new.index_new_command_handler import IndexNewCommandHandler
from domain.new.new_repository import NewRepository


class TestIndexNewCommandHandler(TestCase):
    def setUp(self) -> None:
        self.new_repository_mock = Mock(spec=NewRepository)
        self.event_bus_mock = Mock(spec=EventBus)
        self.logger_mock = Mock(spec=Logger)
        self.command_handler = IndexNewCommandHandler(self.new_repository_mock, self.event_bus_mock, self.logger_mock)

    @patch("application.index_new.index_new_command_handler.uuid4")
    def test_handle_success_non_already_existing(self, uuid_mock):
        test_uuid = uuid4()
        uuid_mock.return_value = test_uuid
        self.new_repository_mock.find_by_title.return_value = None
        test_command = IndexNewCommand(
            title="test_title",
            url="test_url",
            sentiment=12.23,
            source_name="test_source",
            named_entities=[
                {"text": "test_named_entity_1", "type": "test_type_1"},
                {"text": "test_named_entity_2", "type": "test_type_1"},
                {"text": "test_named_entity_3", "type": "test_type_2"},
            ],
        )

        self.command_handler.handle(test_command)

        indexed_new = New(
            id=test_uuid,
            title="test_title",
            url="test_url",
            sentiment=Decimal(12.23),
            source=Source(name="test_source"),
            named_entities=[
                NamedEntity(
                    value="test_named_entity_1", named_entity_type=NamedEntityType(name="test_type_1", description=None)
                ),
                NamedEntity(
                    value="test_named_entity_2", named_entity_type=NamedEntityType(name="test_type_1", description=None)
                ),
                NamedEntity(
                    value="test_named_entity_3", named_entity_type=NamedEntityType(name="test_type_2", description=None)
                ),
            ],
        )
        self.new_repository_mock.save.assert_called_once_with(indexed_new)
        self.new_repository_mock.find_by_title.assert_called_once_with("test_title")
        expected_event = IndexedNewEvent(
            title="test_title",
            url="test_url",
            sentiment=Decimal(12.23),
            source_name="test_source",
            named_entities=[
                {"value": named_entity.value, "type": named_entity.named_entity_type.name}
                for named_entity in indexed_new.named_entities
            ],
        )
        self.event_bus_mock.transport.assert_called_once_with(expected_event)

    def test_handle_success_already_existing(self):
        existing_new = New(
            id=uuid4(),
            title="test_title",
            url="test_url",
            sentiment=Decimal("10.0"),
            source=Source(name="test_source"),
            named_entities=[],
        )
        self.new_repository_mock.find_by_title.return_value = existing_new
        test_command = IndexNewCommand(
            title="test_title",
            url="test_url",
            sentiment=12.23,
            source_name="test_source",
            named_entities=[
                {"text": "test_named_entity_1", "type": "test_type_1"},
                {"text": "test_named_entity_2", "type": "test_type_1"},
                {"text": "test_named_entity_3", "type": "test_type_2"},
            ],
        )

        self.command_handler.handle(test_command)

        indexed_new = New(
            id=existing_new.id,
            title="test_title",
            url="test_url",
            sentiment=Decimal(12.23),
            source=Source(name="test_source"),
            named_entities=[
                NamedEntity(
                    value="test_named_entity_1", named_entity_type=NamedEntityType(name="test_type_1", description=None)
                ),
                NamedEntity(
                    value="test_named_entity_2", named_entity_type=NamedEntityType(name="test_type_1", description=None)
                ),
                NamedEntity(
                    value="test_named_entity_3", named_entity_type=NamedEntityType(name="test_type_2", description=None)
                ),
            ],
        )
        self.new_repository_mock.save.assert_called_once_with(indexed_new)
        self.new_repository_mock.find_by_title.assert_called_once_with("test_title")
        expected_event = IndexedNewEvent(
            title="test_title",
            url="test_url",
            sentiment=Decimal(12.23),
            source_name="test_source",
            named_entities=[
                {"value": named_entity.value, "type": named_entity.named_entity_type.name}
                for named_entity in indexed_new.named_entities
            ],
        )
        self.event_bus_mock.transport.assert_called_once_with(expected_event)
