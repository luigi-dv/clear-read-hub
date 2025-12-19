#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from pymongo import ASCENDING, DESCENDING, AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from src.service_config import ServiceConfig


class DatabaseContext:
    """
    Owns the MongoDB client. One instance is shared by the whole process.
    """

    def __init__(self, client: AsyncMongoClient, database_name: str):
        self.client = client
        self.database: AsyncDatabase = client[database_name]

    @classmethod
    def from_settings(cls, settings: ServiceConfig) -> "DatabaseContext":
        client = AsyncMongoClient(
            settings.MONGODB_URI,
            tz_aware=True,
            serverSelectionTimeoutMS=settings.MONGODB_TIMEOUT_MS,
            appname=settings.SERVICE_NAME,
        )
        return cls(client, settings.MONGODB_DATABASE_NAME)

    async def ensure_indexes(self) -> None:
        await self.database.users.create_index([("email", ASCENDING)], unique=True)
        await self.database.documents.create_index(
            [("owner_id", ASCENDING), ("created_at", DESCENDING)]
        )

    async def ping(self) -> None:
        await self.database.command("ping")

    async def close(self) -> None:
        await self.client.close()
