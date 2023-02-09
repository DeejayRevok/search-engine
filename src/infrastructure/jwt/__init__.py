from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.jwt.jwt_authentication_token_decoder.JWTAuthenticationTokenDecoder",
            "infrastructure.jwt.jwt_authentication_token_decoder.JWTAuthenticationTokenDecoder",
            [Argument.no_kw_argument("@infrastructure.iam.iam_jwt_signing_key_fetcher.IAMJWTSigningKeyFetcher")],
        )
    )
