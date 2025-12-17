#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from datetime import UTC, datetime


def utc_now() -> datetime:
    """
    Current UTC time, truncated to milliseconds: the precision MongoDB stores.

    Timestamps then survive a round trip to the database unchanged.
    """
    now = datetime.now(UTC)
    return now.replace(microsecond=now.microsecond // 1000 * 1000)
