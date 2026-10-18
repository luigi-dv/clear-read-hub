#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
In-memory implementations of the domain ports, used by the unit and API tests.
"""

from datetime import datetime

from src.module.domain.clock import utc_now
from src.module.domain.entities.documents.document import (
    Document,
    DocumentStatus,
    DocumentText,
)
from src.module.domain.entities.security.user import User
from src.module.domain.exceptions import (
    ConflictError,
    NotFoundError,
    StorageObjectNotFoundError,
)
from src.module.domain.repositories.documents.document_repository import (
    IDocumentRepository,
)
from src.module.domain.repositories.files.file_storage import IFileStorage
from src.module.domain.repositories.security.user_repository import IUserRepository
from src.module.domain.services.documents.processing_queue import (
    DocumentProcessingQueue,
)


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users: dict[str, User] = {}

    async def find_by_id(self, user_id: str) -> User | None:
        user = self.users.get(user_id)
        return user.model_copy() if user else None

    async def find_by_email(self, email: str) -> User | None:
        return next(
            (u.model_copy() for u in self.users.values() if u.email == email), None
        )

    async def create(self, user: User) -> User:
        if any(u.email == user.email for u in self.users.values()):
            raise ConflictError("A user with this email already exists.")
        self.users[user.id] = user.model_copy()
        return user

    async def update(self, user: User) -> User:
        if user.id not in self.users:
            raise NotFoundError("User not found.")
        if any(u.email == user.email and u.id != user.id for u in self.users.values()):
            raise ConflictError("A user with this email already exists.")
        self.users[user.id] = user.model_copy()
        return user

    async def delete(self, user_id: str) -> bool:
        return self.users.pop(user_id, None) is not None

    async def ping(self) -> None:
        return None


class InMemoryDocumentRepository(IDocumentRepository):
    def __init__(self):
        self.documents: dict[str, Document] = {}
        self.texts: dict[str, DocumentText] = {}

    async def create(self, document: Document) -> Document:
        self.documents[document.id] = document.model_copy()
        return document

    async def get(self, document_id: str) -> Document | None:
        document = self.documents.get(document_id)
        return document.model_copy() if document else None

    async def list_by_owner(
        self, owner_id: str, limit: int, offset: int = 0
    ) -> list[Document]:
        owned = sorted(
            (d for d in self.documents.values() if d.owner_id == owner_id),
            key=lambda d: (d.created_at, d.id),
            reverse=True,
        )
        return [d.model_copy() for d in owned[offset : offset + limit]]

    async def update(self, document: Document) -> Document:
        if document.id not in self.documents:
            raise NotFoundError("Document not found.")
        self.documents[document.id] = document.model_copy()
        return document

    async def claim_for_processing(
        self, document_id: str, stale_before: datetime
    ) -> Document | None:
        document = self.documents.get(document_id)
        if document is None:
            return None
        claimable = document.status in (
            DocumentStatus.PENDING,
            DocumentStatus.FAILED,
        ) or (
            document.status == DocumentStatus.PROCESSING
            and document.updated_at < stale_before
        )
        if not claimable:
            return None
        document.status = DocumentStatus.PROCESSING
        document.updated_at = utc_now()
        return document.model_copy()

    async def delete(self, document_id: str) -> bool:
        self.texts.pop(document_id, None)
        return self.documents.pop(document_id, None) is not None

    async def save_text(self, text: DocumentText) -> None:
        self.texts[text.document_id] = text.model_copy()

    async def get_text(self, document_id: str) -> DocumentText | None:
        return self.texts.get(document_id)


class InMemoryFileStorage(IFileStorage):
    def __init__(self):
        self.files: dict[str, bytes] = {}
        self.available = True

    async def initialize(self) -> None:
        return None

    async def save(self, key: str, content: bytes, content_type: str) -> None:
        self.files[key] = content

    async def read(self, key: str) -> bytes:
        try:
            return self.files[key]
        except KeyError as e:
            raise StorageObjectNotFoundError() from e

    async def delete(self, key: str) -> None:
        self.files.pop(key, None)

    async def ping(self) -> None:
        if not self.available:
            raise ConnectionError("storage unavailable")


class RecordingQueue(DocumentProcessingQueue):
    """
    Records enqueued documents without processing them.
    """

    def __init__(self, fail: bool = False):
        self.enqueued: list[str] = []
        self.fail = fail

    async def enqueue(self, document_id: str) -> None:
        if self.fail:
            raise ConnectionError("queue unavailable")
        self.enqueued.append(document_id)

    async def ping(self) -> None:
        if self.fail:
            raise ConnectionError("queue unavailable")
