#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import asyncio

from redis import Redis
from rq import Queue, Retry

from src.module.domain.services.documents.processing_queue import (
    DocumentProcessingQueue,
)

PROCESS_DOCUMENT_JOB = (
    "src.module.infrastructure.message_queue.jobs.process_document_job"
)

# Seconds to wait before each retry
_RETRY_INTERVALS = [10, 30, 60, 120, 300]


class RQProcessingQueue(DocumentProcessingQueue):
    """
    Sends documents to a Redis Queue (RQ), processed by `worker.py`.
    """

    def __init__(
        self,
        connection: Redis,
        queue_name: str,
        job_timeout_seconds: int,
        max_retries: int,
    ):
        self.connection = connection
        self.queue = Queue(queue_name, connection=connection)
        self.job_timeout_seconds = job_timeout_seconds
        self.max_retries = max_retries

    async def enqueue(self, document_id: str) -> None:
        retry = None
        if self.max_retries > 0:
            retry = Retry(
                max=self.max_retries, interval=_RETRY_INTERVALS[: self.max_retries]
            )
        await asyncio.to_thread(
            self.queue.enqueue,
            PROCESS_DOCUMENT_JOB,
            document_id,
            job_timeout=self.job_timeout_seconds,
            retry=retry,
            description=f"Process document {document_id}",
        )

    async def ping(self) -> None:
        await asyncio.to_thread(self.connection.ping)

    def close(self) -> None:
        self.connection.close()
