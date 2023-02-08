from logging import Logger
from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from application.update_newspaper.update_newspaper_command import UpdateNewspaperCommand
from application.update_newspaper.update_newspaper_command_handler import UpdateNewspaperCommandHandler
from domain.named_entity.find_named_entities_criteria import FindNamedEntitiesCriteria
from domain.named_entity.named_entity import NamedEntity
from domain.named_entity.named_entity_repository import NamedEntityRepository
from domain.named_entity.named_entity_type import NamedEntityType
from domain.newspaper.newspaper import Newspaper
from domain.newspaper.newspaper_repository import NewspaperRepository


class TestUpdateNewspaperCommandHandler(TestCase):
    def setUp(self) -> None:
        self.newspaper_repository_mock = Mock(spec=NewspaperRepository)
        self.named_entity_repository_mock = Mock(spec=NamedEntityRepository)
        self.logger_mock = Mock(spec=Logger)
        self.command_handler = UpdateNewspaperCommandHandler(
            self.newspaper_repository_mock, self.named_entity_repository_mock, self.logger_mock
        )

    def test_handle_success(self):
        test_newspaper = Newspaper(id=uuid4(), name="test_newspaper", user_email="test_user", named_entities=[])
        self.newspaper_repository_mock.find_by_name_and_user_email.return_value = test_newspaper
        test_named_entity = NamedEntity(
            value="test_named_entity",
            named_entity_type=NamedEntityType(name="test_named_entity_type", description="Test"),
        )
        self.named_entity_repository_mock.find_by_criteria.return_value = [test_named_entity]
        test_command = UpdateNewspaperCommand(
            user_email="test_user",
            original_name="test_newspaper",
            new_name="test_new_newspaper",
            new_named_entities_values=["test_named_entity"],
        )

        self.command_handler.handle(test_command)

        self.newspaper_repository_mock.save.assert_called_once_with(
            Newspaper(
                id=test_newspaper.id,
                name="test_new_newspaper",
                user_email="test_user",
                named_entities=[test_named_entity],
            )
        )
        self.newspaper_repository_mock.find_by_name_and_user_email.assert_called_once_with(
            name="test_newspaper", user_email="test_user"
        )
        self.named_entity_repository_mock.find_by_criteria.assert_called_once_with(
            FindNamedEntitiesCriteria(value_in=["test_named_entity"])
        )
