import os

import aiohttp_cors
from aiohttp.web_app import Application
from aiohttp.web_urldispatcher import StaticResource
from graphene import Schema
from yandil.container import default_container

from app.loaders import load_app
from infrastructure.aiohttp.middlewares.apm_middleware import APMMiddleware
from infrastructure.aiohttp.middlewares.authentication_middleware import AuthenticationMiddleware
from infrastructure.aiohttp.middlewares.error_middleware import ErrorMiddleware
from infrastructure.aiohttp.middlewares.log_middleware import LogMiddleware
from infrastructure.graphql.mutations import Mutations
from infrastructure.graphql.queries import Queries
from infrastructure.graphql.setup import setup_graphql_routes

API_VERSION = "1.0"


def load(*_) -> Application:
    load_app()
    app = Application()
    app["host"] = os.environ.get("SEARCH_ENGINE_SERVER__HOST")
    app["port"] = os.environ.get("SEARCH_ENGINE_SERVER__PORT")

    graphql_scheme = Schema(query=Queries, mutation=Mutations)
    setup_graphql_routes(app, graphql_scheme)

    app.middlewares.append(default_container[ErrorMiddleware].middleware)
    app.middlewares.append(default_container[APMMiddleware].middleware)
    app.middlewares.append(default_container[LogMiddleware].middleware)
    app.middlewares.append(default_container[AuthenticationMiddleware].middleware)

    __setup_cors(app)
    return app


def __setup_cors(app: Application):
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*", allow_methods="*"
            )
        },
    )
    for route in list(app.router.routes()):
        if not isinstance(route.resource, StaticResource):
            cors.add(route)
