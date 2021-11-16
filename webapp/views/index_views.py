from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_request import Request
from aiohttp.web_response import Response, json_response
from aiohttp_apispec import docs, request_schema
from dacite import from_dict

from news_service_lib import ClassRouteTableDef, login_required
from news_service_lib.models import New, NamedEntity

from log_config import get_logger
from webapp.container_config import container
from webapp.definitions import API_VERSION
from webapp.request_schemas.index_views_schemas import PostIndexSchema
from models import New as NewModel

ROOT_PATH = '/api/index'
LOGGER = get_logger()
ROUTES = ClassRouteTableDef()


class IndexViews:
    @docs(
        tags=['Indexing'],
        summary="Index",
        description="Index new data",
        security=[{'ApiKeyAuth': []}]
    )
    @request_schema(PostIndexSchema)
    @ROUTES.post(f'/{API_VERSION}{ROOT_PATH}')
    async def index_new(self, request: Request) -> Response:
        @login_required
        async def request_executor(inner_request):
            LOGGER.info('REST request to index new')

            try:
                new_data = from_dict(New, inner_request['data'])
            except Exception as ex:
                raise HTTPBadRequest(text=str(ex)) from ex

            index_service = container.get('index_service')
            indexed_new: NewModel = index_service.index_new(new_data)

            return json_response(dict(indexed_new), status=200)

        return await request_executor(request)


def setup_routes(app: Application):
    ROUTES.clean_routes()
    ROUTES.add_class_routes(IndexViews())
    app.router.add_routes(ROUTES)
