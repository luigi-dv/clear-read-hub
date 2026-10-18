#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
Repository tests against mongomock. The same behaviour is checked against a real
MongoDB in tests/integration.
"""

from datetime import UTC, datetime, timedelta

import pytest
from mongomock_motor import AsyncMongoMockClient

from src.module.domain.entities.documents.document import (
    Document,
    DocumentStatus,
    DocumentText,
)
from src.module.domain.entities.security.user import User
from src.module.domain.exceptions import ConflictError, NotFoundError
from src.module.domain.value_objects.files.file_type import FileType
from src.module.infrastructure.persistence.repositories.mongo_document_repository import (
    MongoDocumentRepository,
)
from src.module.infrastructure.persistence.repositories.mongo_user_repository import (
    MongoUserRepository,
)


@pytest.fixture
async def database():
    database = AsyncMongoMockClient()["test"]
    await database.users.create_index("email", unique=True)
    return database


def _user(email="a@example.com") -> User:
    return User(email=email, hashed_password="hash")


def _document(owner_id="owner", **kwargs) -> Document:
    return Document(
        owner_id=owner_id,
        filename="a.pdf",
        file_type=FileType.PDF,
        size=1,
        sha256="0" * 64,
        storage_key=f"{owner_id}/a.pdf",
        **kwargs,
    )


class TestMongoUserRepository:
    async def test_create_and_find(self, database):
        repository = MongoUserRepository(database)
        user = await repository.create(_user())
        assert await repository.find_by_id(user.id) == user
        assert await repository.find_by_email("a@example.com") == user
        assert await repository.find_by_id("missing") is None

    async def test_duplicate_email_is_a_conflict(self, database):
        repository = MongoUserRepository(database)
        await repository.create(_user())
        with pytest.raises(ConflictError):
            await repository.create(_user())

    async def test_update(self, database):
        repository = MongoUserRepository(database)
        user = await repository.create(_user())
        user.email = "b@example.com"
        await repository.update(user)
        assert (await repository.find_by_id(user.id)).email == "b@example.com"

    async def test_update_missing_user(self, database):
        with pytest.raises(NotFoundError):
            await MongoUserRepository(database).update(_user())

    async def test_delete(self, database):
        repository = MongoUserRepository(database)
        user = await repository.create(_user())
        assert await repository.delete(user.id)
        assert not await repository.delete(user.id)

    async def test_datetimes_are_timezone_aware(self, database):
        repository = MongoUserRepository(database)
        user = await repository.create(_user())
        assert (await repository.find_by_id(user.id)).created_at.tzinfo is not None


class TestMongoDocumentRepository:
    async def test_create_get_update(self, database):
        repository = MongoDocumentRepository(database)
        document = await repository.create(_document())
        document.mark_completed(page_count=1, char_count=3)
        await repository.update(document)
        stored = await repository.get(document.id)
        assert stored.status == DocumentStatus.COMPLETED
        assert stored.file_type == FileType.PDF

    async def test_list_by_owner_is_paginated_newest_first(self, database):
        repository = MongoDocumentRepository(database)
        now = datetime.now(UTC)
        ids = []
        for minutes in range(5):
            document = _document(created_at=now + timedelta(minutes=minutes))
            await repository.create(document)
            ids.append(document.id)
        await repository.create(_document(owner_id="someone-else"))

        first_page = await repository.list_by_owner("owner", limit=2)
        second_page = await repository.list_by_owner("owner", limit=2, offset=2)
        assert [d.id for d in first_page] == ids[::-1][:2]
        assert [d.id for d in second_page] == ids[::-1][2:4]

    async def test_claim_for_processing(self, database):
        repository = MongoDocumentRepository(database)
        document = await repository.create(_document())
        stale_before = datetime.now(UTC) - timedelta(minutes=5)

        claimed = await repository.claim_for_processing(document.id, stale_before)
        assert claimed.status == DocumentStatus.PROCESSING
        # A second worker cannot claim it while it is being processed
        assert await repository.claim_for_processing(document.id, stale_before) is None

    async def test_claim_stale_processing_document(self, database):
        repository = MongoDocumentRepository(database)
        document = _document(status=DocumentStatus.PROCESSING)
        document.updated_at = datetime.now(UTC) - timedelta(hours=1)
        await repository.create(document)
        stale_before = datetime.now(UTC) - timedelta(minutes=5)
        assert await repository.claim_for_processing(document.id, stale_before)

    async def test_completed_documents_are_not_claimed(self, database):
        repository = MongoDocumentRepository(database)
        document = await repository.create(_document(status=DocumentStatus.COMPLETED))
        assert (
            await repository.claim_for_processing(document.id, datetime.now(UTC))
            is None
        )

    async def test_text_is_stored_separately_and_deleted_with_document(self, database):
        repository = MongoDocumentRepository(database)
        document = await repository.create(_document())
        await repository.save_text(DocumentText(document_id=document.id, pages=["a"]))
        await repository.save_text(DocumentText(document_id=document.id, pages=["b"]))
        assert (await repository.get_text(document.id)).pages == ["b"]

        assert await repository.delete(document.id)
        assert await repository.get(document.id) is None
        assert await repository.get_text(document.id) is None
