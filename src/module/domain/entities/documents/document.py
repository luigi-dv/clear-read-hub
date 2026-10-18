#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field

from src.module.domain.clock import utc_now
from src.module.domain.value_objects.files.file_type import FileType


class DocumentStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(BaseModel):
    """
    A file uploaded by a user, together with the state of its processing.
    """

    id: str = Field(default_factory=lambda: uuid4().hex)
    owner_id: str
    filename: str
    file_type: FileType
    size: int
    sha256: str
    storage_key: str
    status: DocumentStatus = DocumentStatus.PENDING
    error: str | None = None
    page_count: int | None = None
    char_count: int | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    processed_at: datetime | None = None

    def mark_completed(self, page_count: int, char_count: int) -> None:
        now = utc_now()
        self.status = DocumentStatus.COMPLETED
        self.error = None
        self.page_count = page_count
        self.char_count = char_count
        self.processed_at = now
        self.updated_at = now

    def mark_failed(self, error: str) -> None:
        self.status = DocumentStatus.FAILED
        # Keep error messages short, they are returned to the client.
        self.error = error[:500]
        self.updated_at = utc_now()


class DocumentText(BaseModel):
    """
    The text extracted from a document, one entry per page.
    """

    document_id: str
    pages: list[str]

    @property
    def char_count(self) -> int:
        return sum(len(page) for page in self.pages)
