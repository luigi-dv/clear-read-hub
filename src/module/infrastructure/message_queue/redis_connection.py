#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from redis import Redis


def get_redis_connection():
    return Redis()
