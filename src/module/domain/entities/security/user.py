#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from src.module.domain.clock import utc_now


class User(BaseModel):
    """
    User entity represents the user of the application.

    The entity only ever holds the password hash. API schemas decide what is exposed.
    """

    id: str = Field(default_factory=lambda: uuid4().hex)
    email: str
    hashed_password: str
    disabled: bool = False
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    def touch(self) -> None:
        self.updated_at = utc_now()
