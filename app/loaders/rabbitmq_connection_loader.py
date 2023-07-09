import os

from bus_station.shared_terminal.broker_connection.connection_parameters.rabbitmq_connection_parameters import (
    RabbitMQConnectionParameters,
)
from bus_station.shared_terminal.factories.kombu_connection_factory import KombuConnectionFactory
from yandil.container import default_container
from kombu.connection import Connection


def load() -> None:
    rabbitmq_host = os.environ.get("SEARCH_ENGINE_RABBIT__HOST")
    rabbitmq_port = os.environ.get("SEARCH_ENGINE_RABBIT__PORT")
    rabbitmq_user = os.environ.get("SEARCH_ENGINE_RABBIT__USER")
    rabbitmq_password = os.environ.get("SEARCH_ENGINE_RABBIT__PASSWORD")
    rabbitmq_connection_parameters = RabbitMQConnectionParameters(
        host=rabbitmq_host, port=rabbitmq_port, username=rabbitmq_user, password=rabbitmq_password, vhost="/"
    )
    rabbitmq_connection = KombuConnectionFactory().get_connection(rabbitmq_connection_parameters)
    default_container[Connection] = rabbitmq_connection
