#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"


from fastapi.routing import APIRouter

"""
    Service Modules
"""
from src.module.application.services.text.text_service import TextService
from src.module.infrastructure.serializers.files.data.file_data_extracted_model import (
    FileDataExtractedModel,
)


class TextExtract:
    def __init__(self):
        self.router = APIRouter()
        self.set_customized_router()

    @staticmethod
    def get_router():
        text_extract_data = TextExtract()
        return text_extract_data.router

    def set_customized_router(self):

        @self.router.post("/extract", response_model=FileDataExtractedModel)
        async def document_extract_data(blob_name: str):
            """
            Extract data and text of a blob by its blob name.

            Parameters:
            - `blob_name` (str): The name of the blob.

            Returns:
            - `FileDataExtractedModel`: A FileDataExtracted Model.

            Raises:
            - `HTTPException`: If the blob is not found.
            """
            service = TextService(blob_name)
            result = service.extract_text_from_pdf()
            return result
