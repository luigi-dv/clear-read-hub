#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
Background worker: processes the documents enqueued by the API (QUEUE_BACKEND=rq).

    python worker.py
"""

from rq import Worker

from src.module.infrastructure.logging.sentry_logging import (
    configure_logging,
    configure_sentry,
)
from src.module.infrastructure.message_queue.redis_connection import (
    get_redis_connection,
)
from src.service_config import get_settings


def main() -> None:
    settings = get_settings()
    configure_logging(settings)
    configure_sentry(settings)
    connection = get_redis_connection(settings.REDIS_URL, socket_timeout=None)
    worker = Worker([settings.QUEUE_NAME], connection=connection)
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    main()
