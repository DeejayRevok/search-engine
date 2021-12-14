from logging import Logger

import sys
from multiprocessing import Process

import lightbus

from infrastructure.repositories.user_repository import UserRepository
from news_service_lib.events.user_events import UserEvents
from news_service_lib.redis_utils import build_redis_url, RedisHealthChecker

from config import config
from log_config import get_logger
from webapp.event_listeners.user_created_listener import UserCreatedListener
from webapp.event_listeners.user_deleted_listener import UserDeletedListener

LOGGER = get_logger()


def event_bus_runner(bus_worker: lightbus.BusPath):
    try:
        bus_worker.client.run_forever()
    except KeyboardInterrupt:
        LOGGER.info("Stopping event bus worker")
        bus_worker.client.stop_loop()


def run_event_bus(
    redis_config: dict, redis_health_checker: RedisHealthChecker, logger: Logger, user_repository: UserRepository
):
    redis_url = build_redis_url(**config.redis)

    if redis_health_checker.health_check():
        LOGGER.info("Starting event bus on %s", redis_url)
        bus = lightbus.create(
            config=dict(
                service_name="search-engine",
                process_name="search-engine-process",
                bus=dict(schema=dict(transport=dict(redis=dict(url=redis_url)))),
                apis=dict(
                    default=dict(
                        event_transport=dict(redis=dict(url=redis_url)),
                        rpc_transport=dict(redis=dict(url=redis_url)),
                        result_transport=dict(redis=dict(url=redis_url)),
                    )
                ),
            )
        )

        bus.client.register_api(UserEvents())

        UserCreatedListener(
            name="handle_user_creation",
            event_api="user",
            event_name="user_created",
            user_repository=user_repository,
            logger=logger,
        ).add_to_bus(bus)
        UserDeletedListener(
            name="handle_user_deletion",
            event_api="user",
            event_name="user_deleted",
            user_repository=user_repository,
            logger=logger,
        ).add_to_bus(bus)

        p = Process(target=event_bus_runner, args=(bus,))
        p.start()
    else:
        logger.error(f"Redis service not available. Exiting...")
        sys.exit(1)
