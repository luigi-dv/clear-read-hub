#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"


"""
    Global Modules
"""
from fastapi import APIRouter

"""
    Routes modules
"""
from src.routers.document.document import Document
from src.routers.health.health import Health
from src.routers.security.oauth_router import OAuth
from src.routers.security.user_router import Users

"""
    Initialize the Router
"""
router = APIRouter()


@router.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "detail": "The API is alive"}


"""
    Health Routes
"""
router.include_router(Health.get_router(), prefix="/health", tags=["Health"])

"""
    Security Routes
"""
router.include_router(OAuth.get_router(), prefix="/oauth2", tags=["Security"])

"""
    Users Routes
"""
router.include_router(Users.get_router(), prefix="/users", tags=["Users"])

"""
    Document Routes
"""
router.include_router(Document.get_router(), prefix="/documents", tags=["Documents"])
