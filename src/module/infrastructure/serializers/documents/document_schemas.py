#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.module.domain.entities.documents.document import DocumentStatus
from src.module.domain.value_objects.files.file_type import FileType


class DocumentPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    file_type: FileType
    size: int
    sha256: str
    status: DocumentStatus
    error: str | None
    page_count: int | None
    char_count: int | None
    created_at: datetime
    updated_at: datetime
    processed_at: datetime | None


class DocumentList(BaseModel):
    items: list[DocumentPublic]
    limit: int
    offset: int


class DocumentTextPublic(BaseModel):
    document_id: str
    page_count: int
    char_count: int
    pages: list[str]
