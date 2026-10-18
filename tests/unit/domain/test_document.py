#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from src.module.domain.entities.documents.document import (
    Document,
    DocumentStatus,
    DocumentText,
)
from src.module.domain.value_objects.files.file_type import FileType


def _document() -> Document:
    return Document(
        owner_id="owner",
        filename="a.pdf",
        file_type=FileType.PDF,
        size=10,
        sha256="0" * 64,
        storage_key="owner/a.pdf",
    )


def test_new_document_is_pending_with_unique_id():
    first, second = _document(), _document()
    assert first.status == DocumentStatus.PENDING
    assert first.id != second.id


def test_mark_completed_clears_error():
    document = _document()
    document.mark_failed("boom")
    document.mark_completed(page_count=2, char_count=40)
    assert document.status == DocumentStatus.COMPLETED
    assert document.error is None
    assert document.page_count == 2
    assert document.processed_at is not None


def test_mark_failed_truncates_long_errors():
    document = _document()
    document.mark_failed("x" * 2000)
    assert document.status == DocumentStatus.FAILED
    assert len(document.error) == 500


def test_document_text_counts_characters():
    assert DocumentText(document_id="d", pages=["ab", "cde"]).char_count == 5
