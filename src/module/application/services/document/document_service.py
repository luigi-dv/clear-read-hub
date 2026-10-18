#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import asyncio
import hashlib
import logging
from typing import BinaryIO

from src.module.domain.entities.documents.document import (
    Document,
    DocumentStatus,
    DocumentText,
)
from src.module.domain.exceptions import (
    DocumentNotReadyError,
    FileTooLargeError,
    NotFoundError,
    UnsupportedFileTypeError,
)
from src.module.domain.repositories.documents.document_repository import (
    IDocumentRepository,
)
from src.module.domain.repositories.files.file_storage import IFileStorage
from src.module.domain.services.documents.processing_queue import (
    DocumentProcessingQueue,
)
from src.module.domain.value_objects.files.file_name import sanitize_file_name
from src.module.domain.value_objects.files.file_size import FileSize
from src.module.domain.value_objects.files.file_type import FileType

logger = logging.getLogger(__name__)

_READ_CHUNK_BYTES = 1024 * 1024
_DELETE_PAGE_SIZE = 100


class DocumentService:
    """
    Upload, list, read and delete the documents of a user.
    """

    def __init__(
        self,
        repository: IDocumentRepository,
        storage: IFileStorage,
        queue: DocumentProcessingQueue,
        max_upload_bytes: int,
    ):
        self.repository = repository
        self.storage = storage
        self.queue = queue
        self.max_upload_bytes = max_upload_bytes

    async def upload(
        self, owner_id: str, filename: str | None, file: BinaryIO
    ) -> Document:
        """
        Validate and store a file, then schedule its processing.

        :param owner_id: The id of the user uploading the file
        :param filename: The client file name, used for display only
        :param file: The file content
        :return: The created document, in the pending state
        """
        content = await asyncio.to_thread(self._read_limited, file)
        size = FileSize(len(content), self.max_upload_bytes).size
        file_type = FileType.sniff(content)
        if file_type is None:
            raise UnsupportedFileTypeError(
                "File type not allowed. Supported types: "
                + ", ".join(t.value for t in FileType)
                + "."
            )

        document = Document(
            owner_id=owner_id,
            filename=sanitize_file_name(filename),
            file_type=file_type,
            size=size,
            sha256=hashlib.sha256(content).hexdigest(),
            storage_key="",
        )
        document.storage_key = f"{owner_id}/{document.id}{file_type.extension}"

        await self.storage.save(document.storage_key, content, file_type.media_type)
        try:
            await self.repository.create(document)
        except Exception:
            # Do not leave orphan files behind when the record cannot be stored
            await self.storage.delete(document.storage_key)
            raise

        try:
            await self.queue.enqueue(document.id)
        except Exception as e:
            logger.exception("Could not enqueue document %s", document.id)
            document.mark_failed(f"Could not schedule processing: {e}")
            await self.repository.update(document)
        return document

    async def list_documents(
        self, owner_id: str, limit: int, offset: int = 0
    ) -> list[Document]:
        return await self.repository.list_by_owner(owner_id, limit, offset)

    async def get_document(self, owner_id: str, document_id: str) -> Document:
        """
        Get a document of the user.

        Documents of other users are reported as not found, so their ids cannot be probed.
        """
        document = await self.repository.get(document_id)
        if document is None or document.owner_id != owner_id:
            raise NotFoundError("Document not found.")
        return document

    async def get_content(
        self, owner_id: str, document_id: str
    ) -> tuple[Document, bytes]:
        document = await self.get_document(owner_id, document_id)
        return document, await self.storage.read(document.storage_key)

    async def get_text(self, owner_id: str, document_id: str) -> DocumentText:
        document = await self.get_document(owner_id, document_id)
        if document.status != DocumentStatus.COMPLETED:
            raise DocumentNotReadyError(
                f"The document is {document.status.value}, its text is not available."
            )
        text = await self.repository.get_text(document_id)
        if text is None:
            raise NotFoundError("Document text not found.")
        return text

    async def delete_document(self, owner_id: str, document_id: str) -> None:
        document = await self.get_document(owner_id, document_id)
        await self.storage.delete(document.storage_key)
        await self.repository.delete(document.id)

    async def delete_all_documents(self, owner_id: str) -> int:
        """
        Delete every document of a user, used when the user account is deleted.

        :return: The number of deleted documents
        """
        deleted = 0
        while documents := await self.repository.list_by_owner(
            owner_id, _DELETE_PAGE_SIZE
        ):
            for document in documents:
                await self.storage.delete(document.storage_key)
                await self.repository.delete(document.id)
                deleted += 1
        return deleted

    def _read_limited(self, file: BinaryIO) -> bytes:
        # Read at most one byte more than allowed, so huge uploads are not loaded
        buffer = bytearray()
        while chunk := file.read(_READ_CHUNK_BYTES):
            buffer.extend(chunk)
            if len(buffer) > self.max_upload_bytes:
                raise FileTooLargeError(
                    "File size exceeds the maximum limit of "
                    f"{self.max_upload_bytes} bytes."
                )
        return bytes(buffer)
