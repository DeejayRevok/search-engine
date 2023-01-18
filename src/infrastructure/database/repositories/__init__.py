from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.database.repositories.sqlalchemy_named_entity_repository.SQLAlchemyNamedEntityRepository",
            "infrastructure.database.repositories.sqlalchemy_named_entity_repository.SQLAlchemyNamedEntityRepository",
            [
                Argument.no_kw_argument("@sqlalchemy.orm.session.Session")
            ]
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.database.repositories.sqlalchemy_new_repository.SQLAlchemyNewRepository",
            "infrastructure.database.repositories.sqlalchemy_new_repository.SQLAlchemyNewRepository",
            [
                Argument.no_kw_argument("@sqlalchemy.orm.session.Session")
            ]
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.database.repositories.sqlalchemy_newspaper_repository.SQLAlchemyNewspaperRepository",
            "infrastructure.database.repositories.sqlalchemy_newspaper_repository.SQLAlchemyNewspaperRepository",
            [
                Argument.no_kw_argument("@sqlalchemy.orm.session.Session")
            ]
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.database.repositories.sqlalchemy_user_repository.SQLAlchemyUserRepository",
            "infrastructure.database.repositories.sqlalchemy_user_repository.SQLAlchemyUserRepository",
            [
                Argument.no_kw_argument("@sqlalchemy.orm.session.Session")
            ]
        )
    )