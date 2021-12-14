from logging import Logger

from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_request import Request
from aiohttp.web_response import Response, json_response
from aiohttp_apispec import docs, request_schema
from dacite import from_dict

from news_service_lib.decorators import login_required
from news_service_lib.models.new import New

from services.index_service import IndexService
from webapp.definitions import API_VERSION
from webapp.request_schemas.index_view_schemas import PostIndexSchema
from models.new import New as NewModel

ROOT_PATH = '/api/index'


class IndexView:
    __ROOT_PATH = '/api/index'

    def __init__(self, web_container: Application, index_service: IndexService, logger: Logger):
        self.__index_service = index_service
        self.__logger = logger
        self.__setup_routes(web_container)

    def __setup_routes(self, web_container: Application) -> None:
        web_container.add_routes(
            [
                web.post(f"/{API_VERSION}{self.__ROOT_PATH}", self.index_new),
            ]
        )

    @docs(
        tags=['Indexing'],
        summary="Index",
        description="Index new data",
        security=[{'ApiKeyAuth': []}]
    )
    @request_schema(PostIndexSchema)
    async def index_new(self, request: Request) -> Response:
        @login_required
        async def request_executor(inner_request):
            self.__logger.info('REST request to index new')

            try:
                new_data = from_dict(New, inner_request['data'])
            except Exception as ex:
                raise HTTPBadRequest(text=str(ex)) from ex

            indexed_new: NewModel = await self.__index_service.index_new(new_data)

            return json_response(dict(indexed_new), status=200)

        return await request_executor(request)
