#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import pytest

from src.module.application.services.security.user_service import UserService
from src.module.domain.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
)


@pytest.fixture
def service(user_repository, password_hasher, token_service) -> UserService:
    return UserService(user_repository, password_hasher, token_service)


async def test_register_stores_only_the_hash(service, user_repository):
    user = await service.register(" Reader@Example.com ", "password-123")
    stored = user_repository.users[user.id]
    assert stored.email == "reader@example.com"
    assert stored.hashed_password != "password-123"
    assert stored.hashed_password.startswith("$2")


async def test_register_duplicate_email(service):
    await service.register("reader@example.com", "password-123")
    with pytest.raises(ConflictError):
        await service.register("READER@example.com", "password-456")


async def test_authenticate_returns_token_for_user(service, token_service):
    user = await service.register("reader@example.com", "password-123")
    token = await service.authenticate("reader@example.com", "password-123")
    assert token_service.verify(token.access_token) == user.id


@pytest.mark.parametrize(
    ("email", "password"),
    [("reader@example.com", "wrong-password"), ("nobody@example.com", "x")],
)
async def test_authenticate_rejects_bad_credentials(service, email, password):
    await service.register("reader@example.com", "password-123")
    with pytest.raises(AuthenticationError, match="Incorrect email or password"):
        await service.authenticate(email, password)


async def test_disabled_user_cannot_log_in_or_use_tokens(service, user_repository):
    user = await service.register("reader@example.com", "password-123")
    token = await service.authenticate("reader@example.com", "password-123")
    user_repository.users[user.id].disabled = True

    with pytest.raises(AuthenticationError):
        await service.authenticate("reader@example.com", "password-123")
    with pytest.raises(AuthenticationError):
        await service.get_current_user(token.access_token)


async def test_get_current_user(service):
    user = await service.register("reader@example.com", "password-123")
    token = await service.authenticate("reader@example.com", "password-123")
    assert (await service.get_current_user(token.access_token)).id == user.id


async def test_token_of_deleted_user_is_rejected(service):
    user = await service.register("reader@example.com", "password-123")
    token = await service.authenticate("reader@example.com", "password-123")
    await service.delete_user(user.id)
    with pytest.raises(AuthenticationError):
        await service.get_current_user(token.access_token)


async def test_change_password_requires_current_password(service):
    user = await service.register("reader@example.com", "password-123")
    with pytest.raises(AuthenticationError):
        await service.update_user(user, current_password=None, password="new-pass-1")
    with pytest.raises(AuthenticationError):
        await service.update_user(user, current_password="wrong", password="new-pass-1")

    await service.update_user(
        user, current_password="password-123", password="new-pass-1"
    )
    await service.authenticate("reader@example.com", "new-pass-1")


async def test_change_email(service):
    user = await service.register("reader@example.com", "password-123")
    await service.update_user(user, current_password=None, email="New@Example.com")
    await service.authenticate("new@example.com", "password-123")


async def test_delete_missing_user(service):
    with pytest.raises(NotFoundError):
        await service.delete_user("missing")
