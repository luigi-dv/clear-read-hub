#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from collections.abc import Callable, Iterator

import pymupdf
import pytest
from fastapi.testclient import TestClient

from src.module.application.services.document.document_processing_service import (
    DocumentProcessingService,
)
from src.module.infrastructure.container import Container
from src.module.infrastructure.fastapi_init import get_application
from src.module.infrastructure.message_queue.inline_queue import InlineProcessingQueue
from src.module.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from src.module.infrastructure.security.jwt_token_service import JwtTokenService
from src.module.infrastructure.text_extraction.pymupdf_text_extractor import (
    PyMuPDFTextExtractor,
)
from src.service_config import Environment, ServiceConfig
from tests.fakes import (
    InMemoryDocumentRepository,
    InMemoryFileStorage,
    InMemoryUserRepository,
)

TEST_SECRET = "test-secret-key-that-is-long-enough-1234"
TEST_PASSWORD = "correct-horse-battery"


@pytest.fixture
def settings() -> ServiceConfig:
    return ServiceConfig(
        _env_file=None,
        JWT_SECRET_KEY=TEST_SECRET,
        ENVIRONMENT=Environment.TEST,
        BCRYPT_ROUNDS=4,
        MAX_UPLOAD_BYTES=256 * 1024,
        MAX_PDF_PAGES=20,
        LOG_LEVEL="WARNING",
    )


@pytest.fixture
def password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher(rounds=4)


@pytest.fixture
def token_service(settings) -> JwtTokenService:
    return JwtTokenService(TEST_SECRET, "HS256", 15)


@pytest.fixture
def user_repository() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def document_repository() -> InMemoryDocumentRepository:
    return InMemoryDocumentRepository()


@pytest.fixture
def storage() -> InMemoryFileStorage:
    return InMemoryFileStorage()


@pytest.fixture
def processing_service(
    settings, document_repository, storage
) -> DocumentProcessingService:
    return DocumentProcessingService(
        document_repository,
        storage,
        PyMuPDFTextExtractor(max_pages=settings.MAX_PDF_PAGES),
        processing_timeout_seconds=settings.JOB_TIMEOUT_SECONDS,
    )


@pytest.fixture
def container(
    settings,
    user_repository,
    document_repository,
    storage,
    processing_service,
    password_hasher,
    token_service,
) -> Container:
    return Container(
        settings=settings,
        user_repository=user_repository,
        document_repository=document_repository,
        storage=storage,
        queue=InlineProcessingQueue(processing_service),
        password_hasher=password_hasher,
        token_service=token_service,
    )


@pytest.fixture
def client(settings, container) -> Iterator[TestClient]:
    with TestClient(get_application(settings, container)) as test_client:
        yield test_client


@pytest.fixture
def register(client) -> Callable[..., dict[str, str]]:
    """
    Register a user and return the authorization headers for it.
    """

    def _register(email: str = "reader@example.com", password: str = TEST_PASSWORD):
        response = client.post("/users", json={"email": email, "password": password})
        assert response.status_code == 201, response.text
        token = client.post(
            "/oauth2/token", data={"username": email, "password": password}
        )
        assert token.status_code == 200, token.text
        return {"Authorization": f"Bearer {token.json()['access_token']}"}

    return _register


@pytest.fixture
def auth_headers(register) -> dict[str, str]:
    return register()


def make_pdf(pages: list[str]) -> bytes:
    document = pymupdf.open()
    for text in pages:
        page = document.new_page()
        page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


@pytest.fixture
def pdf_factory() -> Callable[[list[str]], bytes]:
    return make_pdf
