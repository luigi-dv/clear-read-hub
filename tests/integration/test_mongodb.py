#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import asyncio
from datetime import timedelta

import pytest

from src.module.domain.clock import utc_now
from src.module.domain.entities.documents.document import Document, DocumentStatus
from src.module.domain.entities.security.user import User
from src.module.domain.exceptions import ConflictError
from src.module.domain.value_objects.files.file_type import FileType
from src.module.infrastructure.persistence.db_context import DatabaseContext
from src.module.infrastructure.persistence.repositories.mongo_document_repository import (
    MongoDocumentRepository,
)
from src.module.infrastructure.persistence.repositories.mongo_user_repository import (
    MongoUserRepository,
)
from src.service_config import ServiceConfig
from tests.conftest import TEST_SECRET

pytestmark = pytest.mark.integration


@pytest.fixture
async def db_context(mongodb_uri, unique_name):
    settings = ServiceConfig(
        _env_file=None,
        JWT_SECRET_KEY=TEST_SECRET,
        MONGODB_URI=mongodb_uri,
        MONGODB_DATABASE_NAME=unique_name,
    )
    context = DatabaseContext.from_settings(settings)
    await context.ensure_indexes()
    yield context
    await context.client.drop_database(unique_name)
    await context.close()


async def test_ping(db_context):
    await db_context.ping()
    await MongoUserRepository(db_context.database).ping()


async def test_unique_email_index(db_context):
    repository = MongoUserRepository(db_context.database)
    user = await repository.create(User(email="a@example.com", hashed_password="h"))
    assert await repository.find_by_id(user.id) == user
    with pytest.raises(ConflictError):
        await repository.create(User(email="a@example.com", hashed_password="h"))


async def test_concurrent_claims_only_succeed_once(db_context):
    repository = MongoDocumentRepository(db_context.database)
    document = await repository.create(
        Document(
            owner_id="owner",
            filename="a.txt",
            file_type=FileType.TXT,
            size=1,
            sha256="0" * 64,
            storage_key="owner/a.txt",
        )
    )
    stale_before = utc_now() - timedelta(minutes=5)
    results = await asyncio.gather(
        *(repository.claim_for_processing(document.id, stale_before) for _ in range(10))
    )
    claimed = [r for r in results if r is not None]
    assert len(claimed) == 1
    assert claimed[0].status == DocumentStatus.PROCESSING
    # Timestamps survive the round trip unchanged
    stored = await repository.get(document.id)
    assert stored.created_at == document.created_at
