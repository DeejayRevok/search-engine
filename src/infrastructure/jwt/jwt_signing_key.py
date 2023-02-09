from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey


@dataclass(frozen=True)
class JWTSigningKey:
    signing_algorithm: str
    signing_key: RSAPublicKey
