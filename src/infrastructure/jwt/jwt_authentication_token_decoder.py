import jwt

from domain.authentication.authentication_token import AuthenticationToken
from domain.authentication.authentication_token_decoder import AuthenticationTokenDecoder
from infrastructure.jwt.jwt_signing_key import JWTSigningKey
from infrastructure.jwt.jwt_signing_key_fetcher import JWTSigningKeyFetcher


class JWTAuthenticationTokenDecoder(AuthenticationTokenDecoder):
    def __init__(self, jwt_signing_key_fetcher: JWTSigningKeyFetcher):
        self.__jwt_signing_key_fetcher = jwt_signing_key_fetcher

    def decode(self, token_encoded: str) -> AuthenticationToken:
        jwt_signing_key = self.__get_jwt_signing_key()
        decoded_token_data = jwt.decode(
            jwt=token_encoded, key=jwt_signing_key.signing_key, algorithms=[jwt_signing_key.signing_algorithm]
        )
        if "sub" not in decoded_token_data:
            raise ValueError("Missing sub field in authentication token")
        return AuthenticationToken(user_email=decoded_token_data["sub"])

    def __get_jwt_signing_key(self) -> JWTSigningKey:
        jwt_signing_key = self.__jwt_signing_key_fetcher.fetch()
        if jwt_signing_key is None:
            raise ValueError("Missing JWT signing key")
        return jwt_signing_key
