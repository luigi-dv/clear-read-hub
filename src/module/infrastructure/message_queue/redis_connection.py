#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from redis import Redis


def get_redis_connection(redis_url: str, socket_timeout: float | None = 10) -> Redis:
    """
    Create a Redis connection.

    Workers block on the queue for minutes and must pass `socket_timeout=None`.
    """
    return Redis.from_url(
        redis_url, socket_connect_timeout=5, socket_timeout=socket_timeout
    )
