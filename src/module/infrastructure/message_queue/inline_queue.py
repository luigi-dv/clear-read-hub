#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import logging

from src.module.application.services.document.document_processing_service import (
    DocumentProcessingService,
)
from src.module.domain.services.documents.processing_queue import (
    DocumentProcessingQueue,
)

logger = logging.getLogger(__name__)


class InlineProcessingQueue(DocumentProcessingQueue):
    """
    Processes documents right away, inside the API process.

    Meant for development and tests: no Redis or worker is needed, but the upload
    request waits for the processing to finish.
    """

    def __init__(self, processing_service: DocumentProcessingService):
        self.processing_service = processing_service

    async def enqueue(self, document_id: str) -> None:
        try:
            await self.processing_service.process(document_id)
        except Exception:
            # The failure is already recorded on the document
            logger.exception("Inline processing failed for document %s", document_id)

    async def ping(self) -> None:
        return None
