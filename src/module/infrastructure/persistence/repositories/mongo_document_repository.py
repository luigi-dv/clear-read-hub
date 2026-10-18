#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from datetime import UTC, datetime
from typing import Any

from pymongo import DESCENDING, ReturnDocument

from src.module.domain.clock import utc_now
from src.module.domain.entities.documents.document import (
    Document,
    DocumentStatus,
    DocumentText,
)
from src.module.domain.exceptions import NotFoundError
from src.module.domain.repositories.documents.document_repository import (
    IDocumentRepository,
)

_DATETIME_FIELDS = ("created_at", "updated_at", "processed_at")


class MongoDocumentRepository(IDocumentRepository):
    """
    Document repository implementation.

    Document records and their extracted text live in separate collections, so
    listing documents never loads the (possibly large) text.
    """

    def __init__(self, database: Any):
        self.collection = database.documents
        self.texts = database.document_texts

    async def create(self, document: Document) -> Document:
        await self.collection.insert_one(_to_record(document))
        return document

    async def get(self, document_id: str) -> Document | None:
        return _to_document(await self.collection.find_one({"_id": document_id}))

    async def list_by_owner(
        self, owner_id: str, limit: int, offset: int = 0
    ) -> list[Document]:
        cursor = (
            self.collection.find({"owner_id": owner_id})
            .sort([("created_at", DESCENDING), ("_id", DESCENDING)])
            .skip(offset)
            .limit(limit)
        )
        return [_to_document(record) async for record in cursor]

    async def update(self, document: Document) -> Document:
        result = await self.collection.replace_one(
            {"_id": document.id}, _to_record(document)
        )
        if result.matched_count == 0:
            raise NotFoundError("Document not found.")
        return document

    async def claim_for_processing(
        self, document_id: str, stale_before: datetime
    ) -> Document | None:
        record = await self.collection.find_one_and_update(
            {
                "_id": document_id,
                "$or": [
                    {
                        "status": {
                            "$in": [DocumentStatus.PENDING, DocumentStatus.FAILED]
                        }
                    },
                    {
                        "status": DocumentStatus.PROCESSING,
                        "updated_at": {"$lt": stale_before},
                    },
                ],
            },
            {
                "$set": {
                    "status": DocumentStatus.PROCESSING,
                    "updated_at": utc_now(),
                }
            },
            return_document=ReturnDocument.AFTER,
        )
        return _to_document(record)

    async def delete(self, document_id: str) -> bool:
        await self.texts.delete_one({"_id": document_id})
        result = await self.collection.delete_one({"_id": document_id})
        return result.deleted_count > 0

    async def save_text(self, text: DocumentText) -> None:
        await self.texts.replace_one(
            {"_id": text.document_id},
            {"_id": text.document_id, "pages": text.pages},
            upsert=True,
        )

    async def get_text(self, document_id: str) -> DocumentText | None:
        record = await self.texts.find_one({"_id": document_id})
        if record is None:
            return None
        return DocumentText(document_id=record["_id"], pages=record["pages"])


def _to_record(document: Document) -> dict:
    record = document.model_dump()
    record["_id"] = record.pop("id")
    return record


def _to_document(record: dict | None) -> Document | None:
    if record is None:
        return None
    record = dict(record)
    record["id"] = record.pop("_id")
    for key in _DATETIME_FIELDS:
        value = record.get(key)
        if isinstance(value, datetime) and value.tzinfo is None:
            record[key] = value.replace(tzinfo=UTC)
    return Document(**record)
