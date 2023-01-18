from logging import Logger
from typing import Optional

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from requests import get, HTTPError

from infrastructure.jwt.jwt_signing_key import JWTSigningKey
from infrastructure.jwt.jwt_signing_key_fetcher import JWTSigningKeyFetcher


class IAMJWTSigningKeyFetcher(JWTSigningKeyFetcher):
    def __init__(self, iam_jwks_path: str, logger: Logger):
        self.__iam_jwks_path = iam_jwks_path
        self.__logger = logger
        self.__signing_key: Optional[JWTSigningKey] = None

    def fetch(self) -> Optional[JWTSigningKey]:
        if self.__signing_key is not None:
            return self.__signing_key

        signing_key = self.__fetch_key_from_iam()
        self.__signing_key = signing_key
        return signing_key

    def __fetch_key_from_iam(self) -> Optional[JWTSigningKey]:
        try:
            jwks_response = get(self.__iam_jwks_path)
        except OSError:
            self.__logger.warning(f"Error connecting with IAM when fetching jwt signing key")
            return None

        try:
            jwks_response.raise_for_status()
        except HTTPError:
            self.__logger.warning("Wrong response from IAM when fetching jwt signing key")
            return None

        jwt_key_data: Optional[dict] = None
        for jwk in jwks_response.json()["keys"]:
            if jwk["use"] == "sig":
                jwt_key_data = jwk

        if jwt_key_data is None:
            self.__logger.warning("JWT signing not found in IAM jwks response")
            return None

        e = int(jwt_key_data["e"])
        n = int(jwt_key_data["n"])
        algorithm = jwt_key_data["alg"]

        return JWTSigningKey(
            signing_key=RSAPublicNumbers(e, n).public_key(),
            signing_algorithm=algorithm
        )
