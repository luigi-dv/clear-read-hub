#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'


"""
    Global Modules
"""
from fastapi import Depends
from typing import Callable
from fastapi.routing import APIRouter

"""
    API Modules
"""
from src.module.application.services.document_service import DocumentService

router = APIRouter()


class DocumentExtractData(Callable):

    def __init__(self, service: DocumentService = Depends()):
        self.service = service

    @router.post("/data/extract")
    async def document_extract_data(self):
        result = await self.service.get()
        return result
