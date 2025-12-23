#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
Jobs executed by the RQ worker (see `worker.py`).

RQ jobs are synchronous functions: each job runs its own event loop and its own
connections, so it does not depend on state left behind by previous jobs.
"""

import asyncio

from src.module.infrastructure.container import (
    build_processing_service,
    build_storage,
)
from src.module.infrastructure.persistence.db_context import DatabaseContext
from src.service_config import get_settings


def process_document_job(document_id: str) -> str | None:
    return asyncio.run(_process_document(document_id))


async def _process_document(document_id: str) -> str | None:
    settings = get_settings()
    db_context = DatabaseContext.from_settings(settings)
    storage = build_storage(settings)
    try:
        service = build_processing_service(settings, db_context, storage)
        await storage.initialize()
        document = await service.process(document_id)
        return document.status.value if document else None
    finally:
        if hasattr(storage, "close"):
            storage.close()
        await db_context.close()
