#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from datetime import UTC, datetime
from typing import Any

from pymongo.errors import DuplicateKeyError

from src.module.domain.entities.security.user import User
from src.module.domain.exceptions import ConflictError, NotFoundError
from src.module.domain.repositories.security.user_repository import IUserRepository


class MongoUserRepository(IUserRepository):
    """
    User repository implementation
    """

    def __init__(self, database: Any):
        self.database = database
        self.collection = database.users

    async def find_by_id(self, user_id: str) -> User | None:
        return _to_user(await self.collection.find_one({"_id": user_id}))

    async def find_by_email(self, email: str) -> User | None:
        return _to_user(await self.collection.find_one({"email": email}))

    async def create(self, user: User) -> User:
        try:
            await self.collection.insert_one(_to_document(user))
        except DuplicateKeyError as e:
            raise ConflictError("A user with this email already exists.") from e
        return user

    async def update(self, user: User) -> User:
        try:
            result = await self.collection.replace_one(
                {"_id": user.id}, _to_document(user)
            )
        except DuplicateKeyError as e:
            raise ConflictError("A user with this email already exists.") from e
        if result.matched_count == 0:
            raise NotFoundError("User not found.")
        return user

    async def delete(self, user_id: str) -> bool:
        result = await self.collection.delete_one({"_id": user_id})
        return result.deleted_count > 0

    async def ping(self) -> None:
        await self.database.command("ping")


def _to_document(user: User) -> dict:
    document = user.model_dump()
    document["_id"] = document.pop("id")
    return document


def _to_user(document: dict | None) -> User | None:
    if document is None:
        return None
    document = dict(document)
    document["id"] = document.pop("_id")
    for key in ("created_at", "updated_at"):
        document[key] = _as_utc(document[key])
    return User(**document)


def _as_utc(value: datetime) -> datetime:
    # MongoDB stores UTC; clients that are not tz aware return naive datetimes
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value
