from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.database.mappers.sqlalchemy_named_entity_mapper.SQLAlchemyNamedEntityMapper",
            "infrastructure.database.mappers.sqlalchemy_named_entity_mapper.SQLAlchemyNamedEntityMapper",
            [Argument.no_kw_argument("@sqlalchemy.MetaData")],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.database.mappers.sqlalchemy_named_entity_new_table.SQLAlchemyNamedEntityNewTable",
            "infrastructure.database.mappers.sqlalchemy_named_entity_new_table.SQLAlchemyNamedEntityNewTable",
            [Argument.no_kw_argument("@sqlalchemy.MetaData")],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.database.mappers"
            ".sqlalchemy_named_entity_newspaper_table.SQLAlchemyNamedEntityNewspaperTable",
            "infrastructure.database.mappers"
            ".sqlalchemy_named_entity_newspaper_table.SQLAlchemyNamedEntityNewspaperTable",
            [Argument.no_kw_argument("@sqlalchemy.MetaData")],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.database.mappers.sqlalchemy_named_entity_type_mapper.SQLAlchemyNamedEntityTypeMapper",
            "infrastructure.database.mappers.sqlalchemy_named_entity_type_mapper.SQLAlchemyNamedEntityTypeMapper",
            [Argument.no_kw_argument("@sqlalchemy.MetaData")],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.database.mappers.sqlalchemy_new_mapper.SQLAlchemyNewMapper",
            "infrastructure.database.mappers.sqlalchemy_new_mapper.SQLAlchemyNewMapper",
            [
                Argument.no_kw_argument("@sqlalchemy.MetaData"),
                Argument.no_kw_argument(
                    "@infrastructure.database.mappers.sqlalchemy_named_entity_new_table.SQLAlchemyNamedEntityNewTable"
                ),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.database.mappers.sqlalchemy_newspaper_mapper.SQLAlchemyNewspaperMapper",
            "infrastructure.database.mappers.sqlalchemy_newspaper_mapper.SQLAlchemyNewspaperMapper",
            [
                Argument.no_kw_argument("@sqlalchemy.MetaData"),
                Argument.no_kw_argument(
                    "@infrastructure.database.mappers"
                    ".sqlalchemy_named_entity_newspaper_table.SQLAlchemyNamedEntityNewspaperTable"
                ),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.database.mappers.sqlalchemy_source_mapper.SQLAlchemySourceMapper",
            "infrastructure.database.mappers.sqlalchemy_source_mapper.SQLAlchemySourceMapper",
            [Argument.no_kw_argument("@sqlalchemy.MetaData")],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.database.mappers.sqlalchemy_user_mapper.SQLAlchemyUserMapper",
            "infrastructure.database.mappers.sqlalchemy_user_mapper.SQLAlchemyUserMapper",
            [Argument.no_kw_argument("@sqlalchemy.MetaData")],
        )
    )
