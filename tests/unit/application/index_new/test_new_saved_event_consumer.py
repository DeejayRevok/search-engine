from unittest import TestCase
from unittest.mock import Mock, patch

from bus_station.command_terminal.bus.command_bus import CommandBus

from application.index_new.index_new_command import IndexNewCommand
from domain.new.new_saved_event import NewSavedEvent

from application.index_new.new_saved_event_consumer import NewSavedEventConsumer


class TestNewSavedEventConsumer(TestCase):
    def setUp(self) -> None:
        self.command_bus_mock = Mock(spec=CommandBus)
        self.event_consumer = NewSavedEventConsumer(self.command_bus_mock)

    @patch("bus_station.passengers.passenger.uuid4")
    def test_consume(self, *_):
        test_event = NewSavedEvent(
            title="test_title",
            url="test_url",
            source="test_source",
            date=2312332.98,
            language="test_language",
            entities=[{"value": "test_entity", "type": "test_type"}],
            sentiment=1.342,
        )

        self.event_consumer.consume(test_event)

        self.command_bus_mock.transport.assert_called_once_with(
            IndexNewCommand(
                title="test_title",
                url="test_url",
                sentiment=1.342,
                source_name="test_source",
                named_entities=[{"value": "test_entity", "type": "test_type"}],
            )
        )
