#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
Composition root: builds the concrete adapters selected by the configuration.
"""

import logging
from dataclasses import dataclass, field

from src.module.application.services.document.document_processing_service import (
    DocumentProcessingService,
)
from src.module.domain.repositories.documents.document_repository import (
    IDocumentRepository,
)
from src.module.domain.repositories.files.file_storage import IFileStorage
from src.module.domain.repositories.security.user_repository import IUserRepository
from src.module.domain.services.documents.processing_queue import (
    DocumentProcessingQueue,
)
from src.module.domain.services.security.password_hasher import PasswordHasher
from src.module.domain.services.security.token_service import TokenService
from src.module.infrastructure.message_queue.inline_queue import InlineProcessingQueue
from src.module.infrastructure.persistence.db_context import DatabaseContext
from src.module.infrastructure.persistence.repositories.mongo_document_repository import (
    MongoDocumentRepository,
)
from src.module.infrastructure.persistence.repositories.mongo_user_repository import (
    MongoUserRepository,
)
from src.module.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from src.module.infrastructure.security.jwt_token_service import JwtTokenService
from src.module.infrastructure.text_extraction.pymupdf_text_extractor import (
    PyMuPDFTextExtractor,
)
from src.service_config import QueueBackend, ServiceConfig, StorageBackend

logger = logging.getLogger(__name__)


@dataclass
class Container:
    settings: ServiceConfig
    user_repository: IUserRepository
    document_repository: IDocumentRepository
    storage: IFileStorage
    queue: DocumentProcessingQueue
    password_hasher: PasswordHasher
    token_service: TokenService
    db_context: DatabaseContext | None = None
    # Extra resources to close on shutdown
    closeables: list = field(default_factory=list)

    async def startup(self) -> None:
        if self.db_context is not None:
            await self.db_context.ensure_indexes()
        await self.storage.initialize()

    async def shutdown(self) -> None:
        for resource in self.closeables:
            try:
                resource.close()
            except Exception:
                logger.exception("Error closing %r", resource)
        if self.db_context is not None:
            await self.db_context.close()


def build_storage(settings: ServiceConfig) -> IFileStorage:
    if settings.STORAGE_BACKEND == StorageBackend.AZURE:
        # Imported lazily: the Azure SDK is only needed for this backend
        from src.module.infrastructure.storage.azure_blob_storage import (
            AzureBlobStorage,
        )

        return AzureBlobStorage(
            settings.AZ_STORAGE_CONNECTION_STRING.get_secret_value(),
            settings.AZ_STORAGE_CONTAINER_NAME,
        )
    from src.module.infrastructure.storage.local_file_storage import LocalFileStorage

    return LocalFileStorage(settings.LOCAL_STORAGE_PATH)


def build_processing_service(
    settings: ServiceConfig,
    db_context: DatabaseContext,
    storage: IFileStorage | None = None,
) -> DocumentProcessingService:
    return DocumentProcessingService(
        repository=MongoDocumentRepository(db_context.database),
        storage=storage or build_storage(settings),
        extractor=PyMuPDFTextExtractor(max_pages=settings.MAX_PDF_PAGES),
        processing_timeout_seconds=settings.JOB_TIMEOUT_SECONDS,
    )


def build_container(settings: ServiceConfig) -> Container:
    db_context = DatabaseContext.from_settings(settings)
    storage = build_storage(settings)
    closeables = [storage] if hasattr(storage, "close") else []

    if settings.QUEUE_BACKEND == QueueBackend.RQ:
        from src.module.infrastructure.message_queue.redis_connection import (
            get_redis_connection,
        )
        from src.module.infrastructure.message_queue.rq_queue import RQProcessingQueue

        queue = RQProcessingQueue(
            get_redis_connection(settings.REDIS_URL),
            settings.QUEUE_NAME,
            settings.JOB_TIMEOUT_SECONDS,
            settings.JOB_MAX_RETRIES,
        )
        closeables.append(queue)
    else:
        queue = InlineProcessingQueue(
            build_processing_service(settings, db_context, storage)
        )

    return Container(
        settings=settings,
        user_repository=MongoUserRepository(db_context.database),
        document_repository=MongoDocumentRepository(db_context.database),
        storage=storage,
        queue=queue,
        password_hasher=BcryptPasswordHasher(rounds=settings.BCRYPT_ROUNDS),
        token_service=JwtTokenService(
            settings.JWT_SECRET_KEY.get_secret_value(),
            settings.JWT_ALGORITHM,
            settings.JWT_EXPIRES_MINUTES,
        ),
        db_context=db_context,
        closeables=closeables,
    )
