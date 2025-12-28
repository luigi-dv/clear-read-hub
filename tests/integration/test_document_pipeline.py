#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
End to end: API -> MongoDB + Azure storage -> Redis queue -> RQ worker -> MongoDB.
"""

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from rq import Queue, SimpleWorker

from src.module.infrastructure.fastapi_init import get_application
from src.module.infrastructure.message_queue.redis_connection import (
    get_redis_connection,
)
from src.service_config import get_settings
from tests.conftest import TEST_PASSWORD, TEST_SECRET, make_pdf

pytestmark = pytest.mark.integration


@pytest.fixture
def pipeline_settings(
    monkeypatch, mongodb_uri, redis_url, azure_connection_string, unique_name
):
    # The worker job reads its configuration from the environment, like in production
    environment = {
        "JWT_SECRET_KEY": TEST_SECRET,
        "BCRYPT_ROUNDS": "4",
        "MONGODB_URI": mongodb_uri,
        "MONGODB_DATABASE_NAME": unique_name,
        "REDIS_URL": redis_url,
        "QUEUE_BACKEND": "rq",
        "QUEUE_NAME": unique_name,
        "STORAGE_BACKEND": "azure",
        "AZ_STORAGE_CONNECTION_STRING": azure_connection_string,
        "AZ_STORAGE_CONTAINER_NAME": unique_name,
    }
    for name, value in environment.items():
        monkeypatch.setenv(name, value)
    get_settings.cache_clear()
    yield get_settings()
    get_settings.cache_clear()
    MongoClient(mongodb_uri).drop_database(unique_name)


def test_upload_is_processed_by_the_worker(pipeline_settings):
    settings = pipeline_settings
    with TestClient(get_application(settings)) as client:
        assert client.get("/health/ready").status_code == 200

        client.post(
            "/users", json={"email": "reader@example.com", "password": TEST_PASSWORD}
        )
        token = client.post(
            "/oauth2/token",
            data={"username": "reader@example.com", "password": TEST_PASSWORD},
        ).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        upload = client.post(
            "/documents",
            headers=headers,
            files={"file": ("paper.pdf", make_pdf(["Hello from the worker"]))},
        )
        assert upload.status_code == 202
        document_id = upload.json()["id"]
        status = client.get(f"/documents/{document_id}", headers=headers).json()
        assert status["status"] == "pending"

        connection = get_redis_connection(settings.REDIS_URL, socket_timeout=None)
        queue = Queue(settings.QUEUE_NAME, connection=connection)
        SimpleWorker([queue], connection=connection).work(burst=True)

        status = client.get(f"/documents/{document_id}", headers=headers).json()
        assert status["status"] == "completed", status
        text = client.get(f"/documents/{document_id}/text", headers=headers).json()
        assert "Hello from the worker" in text["pages"][0]

        queue.delete(delete_jobs=True)
