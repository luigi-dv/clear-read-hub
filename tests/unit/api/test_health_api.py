#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from fastapi.testclient import TestClient

from src.module.infrastructure.fastapi_init import get_application


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_liveness(client):
    assert client.get("/health/live").json() == {"status": "ok"}


def test_readiness(client):
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["checks"] == {
        "database": "ok",
        "storage": "ok",
        "queue": "ok",
    }


def test_readiness_reports_unavailable_dependency(client, storage):
    storage.available = False
    response = client.get("/health/ready")
    assert response.status_code == 503
    assert response.json()["checks"]["storage"] == "unavailable"


def test_cors_is_enabled_for_configured_origins(settings, container):
    settings.CORS_ALLOWED_ORIGINS = "https://app.example.com"
    with TestClient(get_application(settings, container)) as client:
        response = client.options(
            "/users/me",
            headers={
                "Origin": "https://app.example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
    assert response.headers["access-control-allow-origin"] == "https://app.example.com"


def test_openapi_schema(client):
    schema = client.get("/openapi.json").json()
    assert "/documents" in schema["paths"]
    assert "/oauth2/token" in schema["paths"]
