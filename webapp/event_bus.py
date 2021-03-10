"""
Event bus module
"""
import sys
from multiprocessing import Process
from typing import Optional

import lightbus
from aiohttp.web_app import Application

from news_service_lib.events.user_events import UserEvents
from news_service_lib.redis_utils import build_redis_url, redis_health_check

from log_config import get_logger
from webapp.event_listeners.user_created_listener import UserCreatedListener
from webapp.event_listeners.user_deleted_listener import UserDeletedListener

LOGGER = get_logger()
bus: Optional[lightbus.BusPath] = None


def event_bus_runner(bus_worker: lightbus.BusPath):
    """
    Lightbus event bus worker runner function

    Args:
        bus_worker: bus worker instance to run

    """
    try:
        bus_worker.client.run_forever()
    except KeyboardInterrupt:
        LOGGER.info('Stopping event bus worker')
        bus_worker.client.stop_loop()


def setup_event_bus(app: Application):
    """
    Setup the event bus with the provided application data

    Args:
        app: base web application

    """
    global bus
    redis_url = build_redis_url(**app['config'].get_section('REDIS'))

    if redis_health_check(redis_url):
        LOGGER.info('Starting event bus on %s', redis_url)
        bus = lightbus.create(
            config=dict(
                service_name='search-engine',
                process_name='search-engine-process',
                bus=dict(
                    schema=dict(
                        transport=dict(
                            redis=dict(
                                url=redis_url
                            )
                        )
                    )
                ),
                apis=dict(
                    default=dict(
                        event_transport=dict(
                            redis=dict(
                                url=redis_url
                            )
                        ),
                        rpc_transport=dict(
                            redis=dict(
                                url=redis_url
                            )
                        ),
                        result_transport=dict(
                            redis=dict(
                                url=redis_url
                            )
                        )
                    )
                )
            ))

        bus.client.register_api(UserEvents())

        UserCreatedListener(name='handle_user_creation',
                            event_api='user',
                            event_name='user_created',
                            storage_config=app['config'].get_section('storage')).add_to_bus(bus)
        UserDeletedListener(name='handle_user_deletion',
                            event_api='user',
                            event_name='user_deleted',
                            storage_config=app['config'].get_section('storage')).add_to_bus(bus)

        p = Process(target=event_bus_runner, args=(bus,))
        p.start()
    else:
        LOGGER.error(f'Redis service not available. Exiting...')
        sys.exit(1)
