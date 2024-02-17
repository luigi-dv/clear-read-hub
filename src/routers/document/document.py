#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'

"""
    Global Modules
"""
from fastapi import Depends, UploadFile, File
from fastapi.routing import APIRouter

"""
    API Modules
"""
from src.module.application.services.document_service import DocumentService


class Document:
    """
        Class proxy Document.
    """

    def __init__(self):
        self.router = APIRouter()
        self.get_customized_router()  # Add routes to the router

    @staticmethod
    def get_router():
        document = Document()
        return document.router

    def get_customized_router(self):
        """
        Customized router for Document.
        :return:
        """

        @self.router.get("")
        async def get_document(file_name: str):
            """
            Public method for get document management.

            :return: dict
            """

            service = DocumentService()
            return await service.get_file_url(file_name)

        @self.router.post("")
        async def post_document(file: UploadFile = File(...)):
            """
            Public method for upload documents.

            External Services:
                - Azure Storage

            """
            service = DocumentService()
            return await service.upload_file(file)

        @self.router.put("")
        async def put_document():
            """
            Public method for put document management.

            :return: dict
            """
            return {
                "status": "success",
                "message": "Successfully Request | API Client Reader",
            }

        @self.router.delete("")
        async def delete_document():
            """
            Public method for delete document management.

            :return: dict
            """
            return {
                "status": "success",
                "message": "Successfully Request | API Client Reader",
            }
