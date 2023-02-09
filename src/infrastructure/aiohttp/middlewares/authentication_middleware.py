from typing import Callable, Optional

from aiohttp.web_request import Request
from aiohttp.web_response import Response

from domain.authentication.authentication_token_decoder import AuthenticationTokenDecoder


class AuthenticationMiddleware:
    def __init__(self, authentication_token_decoder: AuthenticationTokenDecoder):
        self.__authentication_token_decoder = authentication_token_decoder

    async def middleware(self, _, handler: Callable):
        async def middleware_handler(request: Request) -> Response:
            auth_token_encoded = await self.__get_authentication_token(request)
            request_user: Optional[dict] = None
            if auth_token_encoded is not None:
                auth_token = self.__authentication_token_decoder.decode(auth_token_encoded)
                request_user = {"email": auth_token.user_email}

            request.user = request_user
            response = await handler(request)
            return response

        return middleware_handler

    async def __get_authentication_token(self, request: Request) -> Optional[str]:
        authorization_header_value = request.headers.get("Authorization")
        if authorization_header_value is None:
            return None

        if "Bearer" not in authorization_header_value:
            raise ValueError(f"Wrong authorization header type, expected Bearer, got {authorization_header_value}")

        authorization_header_components = authorization_header_value.split(" ")
        if len(authorization_header_components) != 2:
            raise ValueError(f"Malformed authorization header: {authorization_header_components}")

        return authorization_header_components[1]
