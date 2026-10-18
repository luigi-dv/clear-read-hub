#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import asyncio
import logging
from datetime import UTC, datetime, timedelta

from src.module.domain.entities.documents.document import Document, DocumentText
from src.module.domain.exceptions import (
    StorageObjectNotFoundError,
    TextExtractionError,
)
from src.module.domain.repositories.documents.document_repository import (
    IDocumentRepository,
)
from src.module.domain.repositories.files.file_storage import IFileStorage
from src.module.domain.services.documents.text_extractor import TextExtractor

logger = logging.getLogger(__name__)


class DocumentProcessingService:
    """
    Turns an uploaded document into extracted text.

    Runs in the background, either inside the API process or in a queue worker.
    """

    def __init__(
        self,
        repository: IDocumentRepository,
        storage: IFileStorage,
        extractor: TextExtractor,
        processing_timeout_seconds: int,
    ):
        self.repository = repository
        self.storage = storage
        self.extractor = extractor
        self.processing_timeout = timedelta(seconds=processing_timeout_seconds)

    async def process(self, document_id: str) -> Document | None:
        """
        Process a document.

        Permanent failures (unreadable file) are recorded on the document and not
        raised, retrying would not help. Unexpected failures are recorded and raised,
        so the queue can retry the job.

        :param document_id: The document id
        :return: The processed document, or None if there was nothing to process
        """
        document = await self.repository.claim_for_processing(
            document_id, stale_before=datetime.now(UTC) - self.processing_timeout
        )
        if document is None:
            logger.info("Document %s is missing or already processed", document_id)
            return None

        try:
            content = await self.storage.read(document.storage_key)
            # PDF parsing is CPU bound
            pages = await asyncio.to_thread(
                self.extractor.extract, content, document.file_type
            )
        except (TextExtractionError, StorageObjectNotFoundError) as e:
            logger.warning("Document %s cannot be processed: %s", document_id, e)
            document.mark_failed(str(e))
            return await self.repository.update(document)
        except Exception as e:
            logger.exception("Unexpected error processing document %s", document_id)
            document.mark_failed("Unexpected processing error, it will be retried.")
            await self.repository.update(document)
            raise e

        text = DocumentText(document_id=document.id, pages=pages)
        await self.repository.save_text(text)
        document.mark_completed(page_count=len(pages), char_count=text.char_count)
        return await self.repository.update(document)
