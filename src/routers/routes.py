#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"


"""
    Global Modules
"""
from fastapi import APIRouter
from src.module.infrastructure.api_responses.success_response import SuccessResponse
from src.module.infrastructure.api_responses.models.success_response_model import (
    SuccessResponseModel,
)


"""
    Routes modules
"""
from src.routers.document.document import Document
from src.routers.security.oauth import OAuth

router = APIRouter()

"""
    General Purpose Routes
"""


@router.get("/", response_model=SuccessResponseModel)
async def root():
    return SuccessResponse(message="API is alive", data={})


"""
    Security Routes
"""
router.include_router(OAuth.get_router(), prefix="/oauth2", tags=["Security"])

"""
    Document Routes
"""
router.include_router(Document.get_router(), prefix="/document", tags=["Documents"])
