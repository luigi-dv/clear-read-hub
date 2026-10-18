#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from datetime import UTC, datetime, timedelta

import jwt

from src.module.domain.entities.security.token import Token
from src.module.domain.exceptions import AuthenticationError
from src.module.domain.services.security.token_service import TokenService

_TOKEN_TYPE = "access"


class JwtTokenService(TokenService):
    """
    Issues signed JSON Web Tokens.
    """

    def __init__(self, secret_key: str, algorithm: str, expires_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires = timedelta(minutes=expires_minutes)

    def issue(self, subject: str) -> Token:
        now = datetime.now(UTC)
        payload = {
            "sub": subject,
            "type": _TOKEN_TYPE,
            "iat": now,
            "exp": now + self.expires,
        }
        access_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return Token(
            access_token=access_token,
            expires_in=int(self.expires.total_seconds()),
        )

    def verify(self, token: str) -> str:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                # Never let the token choose its own algorithm
                algorithms=[self.algorithm],
                options={"require": ["sub", "exp", "iat"]},
            )
        except jwt.PyJWTError as e:
            raise AuthenticationError() from e
        if payload.get("type") != _TOKEN_TYPE or not isinstance(payload["sub"], str):
            raise AuthenticationError()
        return payload["sub"]
