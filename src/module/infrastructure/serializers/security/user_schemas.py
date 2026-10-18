#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from src.module.infrastructure.security.bcrypt_password_hasher import (
    MAX_PASSWORD_BYTES,
)

MIN_PASSWORD_LENGTH = 8


def _check_password_bytes(password: str | None) -> str | None:
    if password is not None and len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise ValueError(f"Password must be at most {MAX_PASSWORD_BYTES} bytes long")
    return password


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=MIN_PASSWORD_LENGTH)

    _check_password = field_validator("password")(_check_password_bytes)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=MIN_PASSWORD_LENGTH)
    current_password: str | None = None

    _check_password = field_validator("password")(_check_password_bytes)


class UserPublic(BaseModel):
    """
    The user as returned by the API. Never includes the password hash.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    disabled: bool
    created_at: datetime
    updated_at: datetime
