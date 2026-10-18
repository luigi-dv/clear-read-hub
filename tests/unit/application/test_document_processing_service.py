#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from datetime import UTC, datetime, timedelta

import pytest

from src.module.domain.entities.documents.document import Document, DocumentStatus
from src.module.domain.value_objects.files.file_type import FileType


async def _store(document_repository, storage, content: bytes, **kwargs) -> Document:
    file_type = FileType.sniff(content) or FileType.PDF
    document = Document(
        owner_id="owner",
        filename="a",
        file_type=file_type,
        size=len(content),
        sha256="0" * 64,
        storage_key=f"owner/{len(document_repository.documents)}",
        **kwargs,
    )
    await storage.save(document.storage_key, content, file_type.media_type)
    return await document_repository.create(document)


async def test_processes_pdf(
    processing_service, document_repository, storage, pdf_factory
):
    document = await _store(
        document_repository, storage, pdf_factory(["Page one", "Page two"])
    )
    processed = await processing_service.process(document.id)

    assert processed.status == DocumentStatus.COMPLETED
    assert processed.page_count == 2
    text = await document_repository.get_text(document.id)
    assert "Page one" in text.pages[0]
    assert processed.char_count == text.char_count


async def test_unreadable_file_fails_without_raising(
    processing_service, document_repository, storage
):
    document = await _store(document_repository, storage, b"%PDF-broken")
    processed = await processing_service.process(document.id)
    assert processed.status == DocumentStatus.FAILED
    assert "corrupt" in processed.error


async def test_missing_file_fails_without_raising(
    processing_service, document_repository, storage
):
    document = await _store(document_repository, storage, b"text")
    await storage.delete(document.storage_key)
    processed = await processing_service.process(document.id)
    assert processed.status == DocumentStatus.FAILED


async def test_unexpected_error_is_recorded_and_raised_for_retry(
    processing_service, document_repository, storage
):
    document = await _store(document_repository, storage, b"text")

    async def broken_read(key):
        raise ConnectionError("storage timeout")

    storage.read = broken_read
    with pytest.raises(ConnectionError):
        await processing_service.process(document.id)
    assert (await document_repository.get(document.id)).status == DocumentStatus.FAILED

    # The retry succeeds once the storage is back
    del storage.read
    processed = await processing_service.process(document.id)
    assert processed.status == DocumentStatus.COMPLETED


async def test_processing_is_idempotent(
    processing_service, document_repository, storage
):
    document = await _store(document_repository, storage, b"text")
    assert await processing_service.process(document.id) is not None
    assert await processing_service.process(document.id) is None


async def test_document_being_processed_is_skipped(
    processing_service, document_repository, storage
):
    document = await _store(
        document_repository, storage, b"text", status=DocumentStatus.PROCESSING
    )
    assert await processing_service.process(document.id) is None


async def test_stale_processing_document_is_recovered(
    processing_service, document_repository, storage
):
    document = await _store(
        document_repository, storage, b"text", status=DocumentStatus.PROCESSING
    )
    document_repository.documents[document.id].updated_at = datetime.now(
        UTC
    ) - timedelta(hours=1)
    processed = await processing_service.process(document.id)
    assert processed.status == DocumentStatus.COMPLETED


async def test_deleted_document_is_skipped(processing_service):
    assert await processing_service.process("missing") is None
