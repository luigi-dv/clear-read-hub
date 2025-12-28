#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
Integration tests run against real services:

    MONGODB_URI=mongodb://localhost:27017
    REDIS_URL=redis://localhost:6379/0
    AZ_STORAGE_CONNECTION_STRING=<Azurite connection string>

    pytest -m integration

Each test is skipped when the service it needs is not configured.
"""

import os
from uuid import uuid4

import pytest


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.skip(f"{name} is not set")
    return value


@pytest.fixture
def mongodb_uri() -> str:
    return require_env("MONGODB_URI")


@pytest.fixture
def redis_url() -> str:
    return require_env("REDIS_URL")


@pytest.fixture
def azure_connection_string() -> str:
    return require_env("AZ_STORAGE_CONNECTION_STRING")


@pytest.fixture
def unique_name() -> str:
    return f"test-{uuid4().hex[:12]}"
