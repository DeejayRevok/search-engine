from unittest import TestCase
from unittest.mock import Mock, patch

from bus_station.command_terminal.bus.command_bus import CommandBus

from application.save_user.save_user_command import SaveUserCommand
from application.save_user.user_created_event_consumer import UserCreatedEventConsumer
from domain.user.user_created_event import UserCreatedEvent


class TestUserCreatedEventConsumer(TestCase):
    def setUp(self) -> None:
        self.command_bus_mock = Mock(spec=CommandBus)
        self.event_consumer = UserCreatedEventConsumer(self.command_bus_mock)

    @patch("bus_station.passengers.passenger.uuid4")
    def test_consume_success(self, *_):
        test_event = UserCreatedEvent(email="test_user_email")

        self.event_consumer.consume(test_event)

        self.command_bus_mock.transport.assert_called_once_with(SaveUserCommand(email="test_user_email"))
