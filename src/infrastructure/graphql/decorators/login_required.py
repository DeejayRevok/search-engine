from typing import Callable

from aiohttp.web_exceptions import HTTPForbidden
from graphql import GraphQLResolveInfo


def login_required(function: Callable):
    def wrapper(*args, **kwargs):
        graphql_info = None
        for arg in args:
            if isinstance(arg, GraphQLResolveInfo):
                graphql_info = arg
                break

        if not graphql_info:
            raise ValueError("GraphQL resolve info not found")

        request = graphql_info.context["request"]
        if request.user is None:
            raise HTTPForbidden(reason="User is not present")

        return function(*args, **kwargs)

    return wrapper
