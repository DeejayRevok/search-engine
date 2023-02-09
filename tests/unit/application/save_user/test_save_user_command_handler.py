from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

from application.save_user.save_user_command import SaveUserCommand
from application.save_user.save_user_command_handler import SaveUserCommandHandler
from domain.user.user import User
from domain.user.user_repository import UserRepository


class TestSaveUserCommandHandler(TestCase):
    def setUp(self) -> None:
        self.user_repository_mock = Mock(spec=UserRepository)
        self.logger_mock = Mock(spec=Logger)
        self.command_handler = SaveUserCommandHandler(self.user_repository_mock, self.logger_mock)

    def test_handle_success(self):
        test_command = SaveUserCommand(email="test_user_email")

        self.command_handler.handle(test_command)

        self.user_repository_mock.save.assert_called_once_with(User(email="test_user_email"))
