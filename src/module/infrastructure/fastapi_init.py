#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

"""
    Global Modules
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

"""
    Core Modules
"""
from src.service_config import ServiceConfig, get_settings

"""
    Infrastructure Modules
"""
from src.module.domain.exceptions import (
    AuthenticationError,
    ConflictError,
    DomainError,
    FileTooLargeError,
    InvalidInputError,
    NotFoundError,
    PermissionDeniedError,
    UnsupportedFileTypeError,
)
from src.module.infrastructure.container import Container, build_container
from src.module.infrastructure.logging.sentry_logging import (
    configure_logging,
    configure_sentry,
)

# Most specific classes first
_STATUS_CODES: list[tuple[type[DomainError], int]] = [
    (FileTooLargeError, 413),
    (UnsupportedFileTypeError, 415),
    (InvalidInputError, 422),
    (NotFoundError, 404),
    (ConflictError, 409),
    (AuthenticationError, 401),
    (PermissionDeniedError, 403),
]


def get_application(
    settings: ServiceConfig | None = None, container: Container | None = None
) -> FastAPI:
    """
    Create the FastAPI application.

    :param settings: The configuration, read from the environment by default
    :param container: Prebuilt dependencies, used by the tests
    """
    settings = settings or get_settings()
    configure_logging(settings)
    configure_sentry(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.container = container or build_container(settings)
        await app.state.container.startup()
        try:
            yield
        finally:
            await app.state.container.shutdown()

    app = FastAPI(
        title=settings.SERVICE_NAME,
        description=settings.SERVICE_DESCRIPTION,
        version=settings.SERVICE_VERSION,
        lifespan=lifespan,
    )

    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.add_exception_handler(DomainError, _domain_error_handler)

    # Imported here to avoid a circular import with the routers
    from src.routers.routes import router

    app.include_router(router)
    app.openapi = __custom_openapi(app)
    return app


async def _domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    status_code = next(
        (code for cls, code in _STATUS_CODES if isinstance(exc, cls)), 400
    )
    headers = {"WWW-Authenticate": "Bearer"} if status_code == 401 else None
    return JSONResponse(
        status_code=status_code, content={"detail": exc.message}, headers=headers
    )


# OpenAPI
def __custom_openapi(custom_app: FastAPI):
    def wrapper():
        if custom_app.openapi_schema:
            return custom_app.openapi_schema
        openapi_schema = get_openapi(
            title=custom_app.title,
            description=custom_app.description,
            version=custom_app.version,
            routes=custom_app.routes,
        )
        http_methods = ["post", "get", "put", "patch", "delete"]
        for method in openapi_schema["paths"]:
            for m in http_methods:
                try:
                    del openapi_schema["paths"][method][m]["responses"]["422"]
                except KeyError:
                    pass
        for schema in list(openapi_schema["components"]["schemas"]):
            if schema in ["HTTPValidationError", "ValidationError"]:
                del openapi_schema["components"]["schemas"][schema]
        custom_app.openapi_schema = openapi_schema
        return custom_app.openapi_schema

    return wrapper
