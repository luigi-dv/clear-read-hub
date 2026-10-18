#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import pytest

from tests.conftest import TEST_PASSWORD


def test_register_does_not_return_password(client):
    response = client.post(
        "/users", json={"email": "reader@example.com", "password": TEST_PASSWORD}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "reader@example.com"
    assert body["disabled"] is False
    assert not {"password", "hashed_password"} & body.keys()


def test_register_duplicate_email(client, register):
    register()
    response = client.post(
        "/users", json={"email": "reader@example.com", "password": TEST_PASSWORD}
    )
    assert response.status_code == 409


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "not-an-email", "password": TEST_PASSWORD},
        {"email": "reader@example.com", "password": "short"},
        {"email": "reader@example.com", "password": "ñ" * 40},  # 80 bytes
        {"email": "reader@example.com"},
    ],
)
def test_register_validates_input(client, payload):
    assert client.post("/users", json=payload).status_code == 422


def test_login_with_wrong_password(client, register):
    register()
    response = client.post(
        "/oauth2/token",
        data={"username": "reader@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_me_requires_authentication(client):
    assert client.get("/users/me").status_code == 401
    response = client.get("/users/me", headers={"Authorization": "Bearer garbage"})
    assert response.status_code == 401


def test_me(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "reader@example.com"


def test_update_email_and_password(client, auth_headers):
    response = client.patch(
        "/users/me",
        headers=auth_headers,
        json={
            "email": "new@example.com",
            "password": "brand-new-password",
            "current_password": TEST_PASSWORD,
        },
    )
    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"
    login = client.post(
        "/oauth2/token",
        data={"username": "new@example.com", "password": "brand-new-password"},
    )
    assert login.status_code == 200


def test_update_password_without_current_password(client, auth_headers):
    response = client.patch(
        "/users/me", headers=auth_headers, json={"password": "brand-new-password"}
    )
    assert response.status_code == 401


def test_update_email_to_existing_email(client, register):
    register("other@example.com")
    headers = register()
    response = client.patch(
        "/users/me", headers=headers, json={"email": "other@example.com"}
    )
    assert response.status_code == 409


def test_delete_user_and_their_documents(client, auth_headers, storage):
    client.post(
        "/documents", headers=auth_headers, files={"file": ("a.txt", b"some text")}
    )
    assert storage.files

    assert client.delete("/users/me", headers=auth_headers).status_code == 204
    assert storage.files == {}
    assert client.get("/users/me", headers=auth_headers).status_code == 401


def test_enumeration_routes_do_not_exist(client, register):
    register()
    assert client.get("/users/reader@example.com").status_code in (404, 405)
