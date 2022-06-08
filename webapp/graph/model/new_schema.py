from typing import List, Tuple

from graphene import Node, Field, Boolean, List as GraphList, String
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphql import ResolveInfo
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import BinaryExpression
from news_service_lib.graph.model.new import New as NewDetail

from log_config import get_logger
from models.named_entity import NamedEntity as NamedEntityModel
from models.new import New as NewModel
from services.news_manager_service import NewsManagerService
from webapp.container_config import container

LOGGER = get_logger()


class NewSchema(SQLAlchemyObjectType):
    class Meta:
        model = NewModel
        interfaces = (Node,)
        exclude_fields = ("source_id",)

    archived = Boolean(description="New archived by the logged in user")
    detail = Field(NewDetail, description="New detailed information")

    @staticmethod
    async def resolve_archived(root, info: ResolveInfo) -> bool:
        user_id: int = info.context["request"].user["id"]
        return any(filter(lambda user: user.id == user_id, root.archived_by))

    @staticmethod
    async def resolve_detail(root, _) -> dict:
        LOGGER.info("Resolving new detail")
        news_manager_service: NewsManagerService = container.get("news_manager_service")
        return await news_manager_service.get_new_by_title(root.title)


class NewFilter(FilterSet):
    class Meta:
        model = NewModel
        fields = {
            "title": [...],
            "sentiment": [...],
        }

    has_any_entity = GraphList(String)

    @classmethod
    def has_any_entity_filter(
        cls, _: ResolveInfo, query: Query, named_entity_values: List[str]
    ) -> Tuple[Query, BinaryExpression]:
        query = query.join(NamedEntityModel, NewModel.named_entities)

        filter_ = NamedEntityModel.value.in_(named_entity_values)

        return query, filter_
