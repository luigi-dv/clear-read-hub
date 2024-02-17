#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

"""
    Global Modules
"""
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

"""
    Core Modules
"""
from src.service_config import serviceConfig

"""
    Infrastructure Modules
"""
from src.module.infrastructure.logging.sentry_logging import SentryLogger

"""
    Tools Modules
"""

# Load Configuration
# response_file = load_config()
# settings = Reader(config_file=response_file)


def get_application() -> FastAPI:
    # FastAPI
    app = __initialize_application()
    # OpenAPI
    app.openapi = __custom_openapi(app)
    return app


def __initialize_application() -> FastAPI:
    # Initialize Sentry
    sentry_sdk.init(
        dsn=serviceConfig.SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        enable_tracing=True,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(transaction_style="endpoint"),
        ],
    )

    # FastAPI
    app = FastAPI(
        title=serviceConfig.SERVICE_NAME,
        description=serviceConfig.SERVICE_DESCRIPTION,
        version=serviceConfig.SERVICE_VERSION,
    )

    # Add Sentry Middleware
    sentry_logger = SentryLogger(app)
    sentry_logger.add_sentry_middleware()

    # Return FastAPI
    return app


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
        http_methods = ["post", "get", "put", "delete"]
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
