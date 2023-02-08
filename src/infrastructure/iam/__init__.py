import os

from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.iam.iam_passenger_json_deserializer.IAMPassengerJSONDeserializer",
            "infrastructure.iam.iam_passenger_json_deserializer.IAMPassengerJSONDeserializer",
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.iam.iam_jwt_signing_key_fetcher.IAMJWTSigningKeyFetcher",
            "infrastructure.iam.iam_jwt_signing_key_fetcher.IAMJWTSigningKeyFetcher",
            [
                Argument.no_kw_argument(os.environ.get("SEARCH_ENGINE_IAM_JWKS_PATH")),
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
