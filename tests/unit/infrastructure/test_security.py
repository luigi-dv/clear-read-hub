#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from datetime import UTC, datetime, timedelta

import jwt
import pytest

from src.module.domain.exceptions import AuthenticationError
from src.module.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from src.module.infrastructure.security.jwt_token_service import JwtTokenService
from tests.conftest import TEST_SECRET


class TestBcryptPasswordHasher:
    def test_hash_and_verify(self, password_hasher):
        hashed = password_hasher.hash_password("s3cret-password")
        assert hashed != "s3cret-password"
        assert password_hasher.verify_password("s3cret-password", hashed)
        assert not password_hasher.verify_password("wrong-password", hashed)

    def test_hashes_are_salted(self, password_hasher):
        assert password_hasher.hash_password("same") != password_hasher.hash_password(
            "same"
        )

    def test_invalid_hash_does_not_verify(self, password_hasher):
        assert not password_hasher.verify_password("anything", "not-a-bcrypt-hash")

    def test_rejects_passwords_longer_than_72_bytes(self):
        with pytest.raises(ValueError):
            BcryptPasswordHasher(rounds=4).hash_password("a" * 73)


class TestJwtTokenService:
    def test_issue_and_verify(self, token_service):
        token = token_service.issue("user-1")
        assert token.token_type == "bearer"
        assert token.expires_in == 15 * 60
        assert token_service.verify(token.access_token) == "user-1"

    def test_rejects_token_signed_with_another_key(self, token_service):
        other = JwtTokenService("another-secret-key-of-enough-length!!", "HS256", 15)
        with pytest.raises(AuthenticationError):
            token_service.verify(other.issue("user-1").access_token)

    def test_rejects_expired_token(self, token_service):
        now = datetime.now(UTC)
        token = jwt.encode(
            {
                "sub": "user-1",
                "type": "access",
                "iat": now - timedelta(hours=1),
                "exp": now - timedelta(minutes=1),
            },
            TEST_SECRET,
            algorithm="HS256",
        )
        with pytest.raises(AuthenticationError):
            token_service.verify(token)

    def test_rejects_unsigned_token(self, token_service):
        token = jwt.encode(
            {"sub": "user-1", "type": "access", "iat": 0, "exp": 9999999999},
            key=None,
            algorithm="none",
        )
        with pytest.raises(AuthenticationError):
            token_service.verify(token)

    def test_rejects_token_without_required_claims(self, token_service):
        token = jwt.encode({"sub": "user-1"}, TEST_SECRET, algorithm="HS256")
        with pytest.raises(AuthenticationError):
            token_service.verify(token)

    def test_rejects_token_of_another_type(self, token_service):
        now = datetime.now(UTC)
        token = jwt.encode(
            {
                "sub": "user-1",
                "type": "refresh",
                "iat": now,
                "exp": now + timedelta(minutes=5),
            },
            TEST_SECRET,
            algorithm="HS256",
        )
        with pytest.raises(AuthenticationError):
            token_service.verify(token)

    def test_rejects_garbage(self, token_service):
        with pytest.raises(AuthenticationError):
            token_service.verify("not.a.token")
