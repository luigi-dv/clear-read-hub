#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import logging

import sentry_sdk

from src.service_config import ServiceConfig


def configure_logging(settings: ServiceConfig) -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL.upper(),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    # The Azure SDK logs every HTTP request and its headers at INFO
    logging.getLogger("azure").setLevel(logging.WARNING)


def configure_sentry(settings: ServiceConfig) -> None:
    """
    Initialize Sentry when a DSN is configured.

    The FastAPI, Starlette and RQ integrations are enabled automatically by the SDK.
    """
    if not settings.SENTRY_DSN:
        return
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT.value,
        release=settings.SERVICE_VERSION,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        send_default_pii=False,
    )
