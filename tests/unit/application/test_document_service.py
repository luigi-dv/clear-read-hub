#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import io

import pytest

from src.module.application.services.document.document_service import DocumentService
from src.module.domain.entities.documents.document import DocumentStatus
from src.module.domain.exceptions import (
    DocumentNotReadyError,
    FileTooLargeError,
    InvalidInputError,
    NotFoundError,
    UnsupportedFileTypeError,
)
from src.module.domain.value_objects.files.file_type import FileType
from tests.fakes import RecordingQueue


@pytest.fixture
def queue() -> RecordingQueue:
    return RecordingQueue()


@pytest.fixture
def service(document_repository, storage, queue) -> DocumentService:
    return DocumentService(document_repository, storage, queue, max_upload_bytes=1024)


async def test_upload_stores_file_and_enqueues(service, storage, queue, pdf_factory):
    service.max_upload_bytes = 1024 * 1024
    content = pdf_factory(["Hello"])
    document = await service.upload("owner", "../thesis.pdf", io.BytesIO(content))

    assert document.status == DocumentStatus.PENDING
    assert document.file_type == FileType.PDF
    assert document.filename == "thesis.pdf"
    assert document.size == len(content)
    assert document.storage_key == f"owner/{document.id}.pdf"
    assert storage.files[document.storage_key] == content
    assert queue.enqueued == [document.id]


async def test_file_name_does_not_decide_the_type(service):
    document = await service.upload("owner", "fake.pdf", io.BytesIO(b"just text"))
    assert document.file_type == FileType.TXT


async def test_rejects_unsupported_content(service, storage):
    with pytest.raises(UnsupportedFileTypeError):
        await service.upload("owner", "a.docx", io.BytesIO(b"PK\x03\x04\x00\x00"))
    assert storage.files == {}


async def test_rejects_empty_file(service):
    with pytest.raises(InvalidInputError):
        await service.upload("owner", "a.txt", io.BytesIO(b""))


async def test_rejects_too_large_file(service, storage):
    with pytest.raises(FileTooLargeError):
        await service.upload("owner", "a.txt", io.BytesIO(b"a" * 1025))
    assert storage.files == {}


async def test_file_is_removed_when_record_cannot_be_stored(
    service, document_repository, storage
):
    async def failing_create(document):
        raise ConnectionError("database down")

    document_repository.create = failing_create
    with pytest.raises(ConnectionError):
        await service.upload("owner", "a.txt", io.BytesIO(b"text"))
    assert storage.files == {}


async def test_document_is_failed_when_queue_is_down(document_repository, storage):
    service = DocumentService(
        document_repository, storage, RecordingQueue(fail=True), 1024
    )
    document = await service.upload("owner", "a.txt", io.BytesIO(b"text"))
    stored = await document_repository.get(document.id)
    assert stored.status == DocumentStatus.FAILED
    assert "Could not schedule processing" in stored.error


async def test_documents_of_other_users_are_not_found(service):
    document = await service.upload("owner", "a.txt", io.BytesIO(b"text"))
    with pytest.raises(NotFoundError):
        await service.get_document("intruder", document.id)
    with pytest.raises(NotFoundError):
        await service.delete_document("intruder", document.id)
    assert (await service.get_document("owner", document.id)).id == document.id


async def test_text_is_not_available_before_processing(service):
    document = await service.upload("owner", "a.txt", io.BytesIO(b"text"))
    with pytest.raises(DocumentNotReadyError):
        await service.get_text("owner", document.id)


async def test_delete_removes_file_and_record(service, storage, document_repository):
    document = await service.upload("owner", "a.txt", io.BytesIO(b"text"))
    await service.delete_document("owner", document.id)
    assert storage.files == {}
    assert await document_repository.get(document.id) is None


async def test_delete_all_documents(service, storage, document_repository):
    for i in range(3):
        await service.upload("owner", f"{i}.txt", io.BytesIO(b"text"))
    kept = await service.upload("other", "kept.txt", io.BytesIO(b"text"))

    assert await service.delete_all_documents("owner") == 3
    assert list(storage.files) == [kept.storage_key]
    assert list(document_repository.documents) == [kept.id]
