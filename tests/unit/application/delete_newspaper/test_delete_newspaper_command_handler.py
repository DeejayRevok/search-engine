from logging import Logger
from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from application.delete_newspaper.delete_newspaper_command import DeleteNewspaperCommand
from application.delete_newspaper.delete_newspaper_command_handler import DeleteNewspaperCommandHandler
from domain.newspaper.newspaper_repository import NewspaperRepository


class DeleteNewspaperCommandHandlerTest(TestCase):
    def setUp(self) -> None:
        self.newspaper_repository_mock = Mock(spec=NewspaperRepository)
        self.logger_mock = Mock(spec=Logger)
        self.command_handler = DeleteNewspaperCommandHandler(self.newspaper_repository_mock, self.logger_mock)

    def test_handle_success(self):
        test_newspaper_id = uuid4()
        test_command = DeleteNewspaperCommand(newspaper_id=str(test_newspaper_id))

        self.command_handler.handle(test_command)

        self.newspaper_repository_mock.delete.assert_called_once_with(test_newspaper_id)
