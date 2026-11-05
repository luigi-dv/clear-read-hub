#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import pytest

from src.service_config import ServiceConfig


@pytest.fixture(autouse=True)
def isolated_environment(monkeypatch):
    """
    Unit tests never read the configuration of the machine running them.

    The integration test services (MONGODB_URI, AZ_STORAGE_CONNECTION_STRING...) are
    set in the environment of CI and of the Docker test container.
    """
    for name in ServiceConfig.model_fields:
        monkeypatch.delenv(name, raising=False)
