#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from abc import ABC, abstractmethod
from datetime import datetime

from src.module.domain.entities.documents.document import Document, DocumentText


class IDocumentRepository(ABC):

    @abstractmethod
    async def create(self, document: Document) -> Document:
        """
        Store a new document record
        """

    @abstractmethod
    async def get(self, document_id: str) -> Document | None:
        """
        Get a document by its id
        :return: The document, or None if it does not exist
        """

    @abstractmethod
    async def list_by_owner(
        self, owner_id: str, limit: int, offset: int = 0
    ) -> list[Document]:
        """
        List the documents of a user, newest first
        """

    @abstractmethod
    async def update(self, document: Document) -> Document:
        """
        Replace a document record
        :raises NotFoundError: If the document does not exist
        """

    @abstractmethod
    async def claim_for_processing(
        self, document_id: str, stale_before: datetime
    ) -> Document | None:
        """
        Atomically move a document to the processing state.

        Pending and failed documents can be claimed, as well as documents stuck in
        processing since before `stale_before` (the worker died). Two workers
        receiving the same job can never process the same document at the same time.

        :return: The claimed document, or None if it is missing or not claimable
        """

    @abstractmethod
    async def delete(self, document_id: str) -> bool:
        """
        Delete a document record and its extracted text
        :return: True if a document was deleted
        """

    @abstractmethod
    async def save_text(self, text: DocumentText) -> None:
        """
        Store (or replace) the text extracted from a document
        """

    @abstractmethod
    async def get_text(self, document_id: str) -> DocumentText | None:
        """
        Get the text extracted from a document
        """
