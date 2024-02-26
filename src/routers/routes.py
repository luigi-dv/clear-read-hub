#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"


"""
    Global Modules
"""
from fastapi import APIRouter, HTTPException

"""
    Routes modules
"""
from src.routers.document.document import Document
from src.routers.security.oauth_router import OAuth
from src.routers.security.user_router import Users
from src.routers.text.extract import TextExtractData

"""
    Initialize the Router
"""
router = APIRouter()


@router.get("/")
async def root():
    raise HTTPException(status_code=200, detail="The API is alive")


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
router.include_router(Document.get_router(), prefix="/document", tags=["Documents"])

"""
    Text Routes
"""
router.include_router(TextExtractData.get_router(), prefix="/text", tags=["Processing"])
