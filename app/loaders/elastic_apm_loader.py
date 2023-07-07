from logging import ERROR

from elasticapm import Client
from elasticapm.utils.logging import get_logger
from yandil.configuration.configuration_container import default_configuration_container
from yandil.configuration.environment import Environment
from yandil.container import default_container


def load() -> None:
    get_logger("elasticapm").setLevel(ERROR)

    default_configuration_container["transactions_ignore_patterns"] = ["^OPTIONS "]
    default_configuration_container["service_name"] = "search-engine"

    default_container.add(Client)
