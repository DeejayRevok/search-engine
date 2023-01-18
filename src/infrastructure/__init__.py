from infrastructure.database import load as load_database
from infrastructure.aiohttp import load as load_aiohttp
from infrastructure.graphql import load as load_graphql
from infrastructure.iam import load as load_iam
from infrastructure.jwt import load as load_jwt


def load() -> None:
    load_aiohttp()
    load_graphql()
    load_database()
    load_iam()
    load_jwt()
