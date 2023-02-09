import os

from bus_station.shared_terminal.broker_connection.connection_parameters.rabbitmq_connection_parameters import (
    RabbitMQConnectionParameters,
)
from bus_station.shared_terminal.factories.kombu_connection_factory import KombuConnectionFactory
from pypendency.builder import container_builder


def load() -> None:
    rabbitmq_host = os.environ.get("SEARCH_ENGINE_RABBIT__HOST")
    rabbitmq_port = os.environ.get("SEARCH_ENGINE_RABBIT__PORT")
    rabbitmq_user = os.environ.get("SEARCH_ENGINE_RABBIT__USER")
    rabbitmq_password = os.environ.get("SEARCH_ENGINE_RABBIT__PASSWORD")
    rabbitmq_connection_parameters = RabbitMQConnectionParameters(
        host=rabbitmq_host, port=rabbitmq_port, username=rabbitmq_user, password=rabbitmq_password, vhost="/"
    )
    rabbitmq_connection = KombuConnectionFactory().get_connection(rabbitmq_connection_parameters)
    container_builder.set("kombu.connection.Connection", rabbitmq_connection)
