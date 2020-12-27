"""
Index views module
"""
from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_request import Request
from aiohttp.web_response import Response, json_response
from aiohttp_apispec import docs, request_schema
from news_service_lib import ClassRouteTableDef, login_required
from news_service_lib.models import New, NamedEntity

from log_config import get_logger
from services.index_service import IndexService
from webapp.definitions import API_VERSION
from webapp.request_schemas.index_views_schemas import PostIndexSchema
from models import New as NewModel

ROOT_PATH = '/api/index'
LOGGER = get_logger()
ROUTES = ClassRouteTableDef()


class IndexViews:
    """
    Index REST endpoint views handler
    """

    def __init__(self, app: Application):
        """
        Initialize the news views handler

        Args:
            app: application associated
        """
        self._index_service: IndexService = app['index_service']

    @docs(
        tags=['Indexing'],
        summary="Index",
        description="Index new data",
        security=[{'ApiKeyAuth': []}]
    )
    @request_schema(PostIndexSchema)
    @ROUTES.post(f'/{API_VERSION}{ROOT_PATH}')
    async def index_new(self, request: Request) -> Response:
        """
        Request to index new

        Args:
            request: input REST request

        Returns: json REST response with the indexed new title

        """

        @login_required
        async def request_executor(inner_request):
            LOGGER.info('REST request to index new')

            try:
                new_data = New(title=inner_request['data']['title'],
                               content=inner_request['data']['content'],
                               source=inner_request['data']['source'],
                               date=inner_request['data']['date'],
                               hydrated=inner_request['data']['hydrated'],
                               summary=inner_request['data']['summary'],
                               sentiment=inner_request['data']['sentiment'],
                               entities=[NamedEntity(**entity) for entity in inner_request['data']['entities']])
            except Exception as ex:
                raise HTTPBadRequest(text=str(ex)) from ex

            indexed_new: NewModel = await self._index_service.index_new(new_data)

            return json_response(dict(indexed_new), status=200)

        return await request_executor(request)


def setup_routes(app: Application):
    """
    Add the class routes to the specified application

    Args:
        app: application to add routes

    """
    ROUTES.clean_routes()
    ROUTES.add_class_routes(IndexViews(app))
    app.router.add_routes(ROUTES)
