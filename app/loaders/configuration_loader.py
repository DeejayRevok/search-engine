from yandil.configuration.configuration_container import default_configuration_container
from yandil.configuration.environment import Environment


def load() -> None:
    default_configuration_container["iam_jwks_path"] = Environment("SEARCH_ENGINE_IAM_JWKS_PATH")
    default_configuration_container["secret_token"] = Environment("SEARCH_ENGINE_ELASTIC_APM__SECRET_TOKEN")
    default_configuration_container["server_url"] = Environment("SEARCH_ENGINE_ELASTIC_APM__URL")
