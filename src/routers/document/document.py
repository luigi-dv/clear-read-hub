#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"


from fastapi import UploadFile, File
from fastapi.routing import APIRouter
from src.module.application.services.document.document_service import DocumentService


class Document:
    """
    Class proxy Document.
    """

    def __init__(self):
        self.router = APIRouter()
        self.set_customized_router()  # Add routes to the router

    @staticmethod
    def get_router():
        document = Document()
        return document.router

    def set_customized_router(self):
        """
        Customized router for Document.
        """

        @self.router.get("")
        async def get_document(file_name: str):
            """
            Retrieve the URL of a document by its file name.

            Parameters:
            - `file_name` (str): The name of the document.

            Returns:
            - `Dict[str, str]`: A dictionary with the URL of the requested document.

            Raises:
            - `HTTPException`: If the document is not found.
            """

            service = DocumentService()
            return await service.get_document_url(file_name)

        @self.router.post("")
        async def post_document(file: UploadFile = File(...)):
            """
            Upload a new document.

            Parameters:
            - `file` (UploadFile): The file to be uploaded.

            Returns:
            - `Dict[str, str]`: A dictionary with the status and message of the upload process.

            Raises:
            - `HTTPException`: If the upload fails.
            """

            service = DocumentService()
            return await service.upload_file(file)

        @self.router.put("")
        async def put_document():
            """
            Placeholder route for document management via HTTP PUT method.

            Returns:
            - `Dict[str, str]`: A dictionary with a success message.

            Note:
            This route does not perform any specific document management with the HTTP PUT method.
            """

            return {
                "status": "success",
                "message": "Successfully Request | API Client Reader",
            }

        @self.router.delete("")
        async def delete_document():
            """
            Placeholder route for document management via HTTP DELETE method.

            Returns:
            - `Dict[str, str]`: A dictionary with a success message.

            Note:
            This route does not perform any specific document deletion with the HTTP DELETE method.
            """

            return {
                "status": "success",
                "message": "Successfully Request | API Client Reader",
            }
