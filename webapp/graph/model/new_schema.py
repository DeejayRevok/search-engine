"""
New models GraphQL module
"""
from graphene import Node, Field, Boolean
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphql import ResolveInfo

from log_config import get_logger
from news_service_lib.graphql.model import New as NewDetail

from models import New as NewModel

LOGGER = get_logger()


class NewSchema(SQLAlchemyObjectType):
    """
    GraphQL new model schema
    """
    class Meta:
        """
        New schema metadata
        """
        model = NewModel
        interfaces = (Node,)
        exclude_fields = ('source_id',)

    archived = Boolean(description='New archived by the logged in user')
    detail = Field(NewDetail, description='New detailed information')

    @staticmethod
    async def resolve_archived(root, info: ResolveInfo) -> bool:
        """
        New schema archived field resolver

        Args:
            root: root new schema instance
            info: query resolver info

        Returns: True if the current logged user has archived this new, False otherwise

        """
        user_id: int = info.context['request'].user['id']
        return any(filter(lambda user: user.id == user_id, root.archived_by))

    @staticmethod
    async def resolve_detail(root, info: ResolveInfo) -> dict:
        """
        New schema detail field resolver

        Args:
            root: root new schema instance
            info: query resolver info

        Returns: root new detail

        """
        LOGGER.info('Resolving new detail')
        app = info.context['request'].app
        return await app['news_manager_service'].get_new_by_title(root.title)


class NewFilter(FilterSet):
    """
    GraphQL new filters schema
    """
    class Meta:
        """
        New filter schema metadata
        """
        model = NewModel
        fields = {
            'title': [...],
            'sentiment': [...],
        }
