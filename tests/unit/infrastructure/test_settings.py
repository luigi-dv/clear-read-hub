#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import pytest
from pydantic import ValidationError

from src.service_config import ServiceConfig, StorageBackend
from tests.conftest import TEST_SECRET


def test_secret_key_is_required(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    with pytest.raises(ValidationError):
        ServiceConfig(_env_file=None)


def test_short_secret_key_is_rejected():
    with pytest.raises(ValidationError):
        ServiceConfig(_env_file=None, JWT_SECRET_KEY="short")


def test_azure_storage_requires_connection_string():
    with pytest.raises(ValidationError, match="AZ_STORAGE_CONNECTION_STRING"):
        ServiceConfig(
            _env_file=None,
            JWT_SECRET_KEY=TEST_SECRET,
            STORAGE_BACKEND=StorageBackend.AZURE,
        )


def test_reads_environment(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", TEST_SECRET)
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "https://a.com, https://b.com,")
    monkeypatch.setenv("QUEUE_BACKEND", "rq")
    settings = ServiceConfig(_env_file=None)
    assert settings.cors_origins == ["https://a.com", "https://b.com"]
    assert settings.QUEUE_BACKEND == "rq"


def test_secret_is_not_printed():
    settings = ServiceConfig(_env_file=None, JWT_SECRET_KEY=TEST_SECRET)
    assert TEST_SECRET not in repr(settings)
