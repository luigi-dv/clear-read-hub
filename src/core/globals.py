#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'

from starlette import status

from src.module.infrastructure.api_responses.error_response import ErrorResponse
from src.module.infrastructure.api_responses.forbidden_response import ForbiddenResponse
from src.module.infrastructure.api_responses.not_found_response import NotFoundResponse
from src.module.infrastructure.api_responses.success_response import SuccessResponse

"""
    Global Modules
"""
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

"""
    Core Modules
"""
from src.core.settings import coresettings

"""
    Tools Modules
"""

# Load Configuration
# response_file = load_config()
# settings = Reader(config_file=response_file)

app = FastAPI(
    title=coresettings.SERVICE_NAME,
    description=coresettings.SERVICE_DESCRIPTION,
    version=coresettings.SERVICE_VERSION,
)


# OpenAPI
def custom_openapi(custom_app: FastAPI):
    def wrapper():
        if custom_app.openapi_schema:
            return custom_app.openapi_schema
        openapi_schema = get_openapi(title=custom_app.title,
                                     description=custom_app.description,
                                     version=custom_app.version,
                                     routes=custom_app.routes)
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



app.openapi = custom_openapi(app)


