from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.aiohttp.middlewares.error_middleware.ErrorMiddleware",
            "infrastructure.aiohttp.middlewares.error_middleware.ErrorMiddleware",
            [
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.aiohttp.middlewares.apm_middleware.APMMiddleware",
            "infrastructure.aiohttp.middlewares.apm_middleware.APMMiddleware",
            [
                Argument.no_kw_argument("@elasticapm.Client"),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.aiohttp.middlewares.log_middleware.LogMiddleware",
            "infrastructure.aiohttp.middlewares.log_middleware.LogMiddleware",
            [
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.aiohttp.middlewares.authentication_middleware.AuthenticationMiddleware",
            "infrastructure.aiohttp.middlewares.authentication_middleware.AuthenticationMiddleware",
            [
                Argument.no_kw_argument(
                    "@infrastructure.jwt.jwt_authentication_token_decoder.JWTAuthenticationTokenDecoder"
                )
            ]
        )
    )
