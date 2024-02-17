#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from sentry_sdk import capture_exception

"""
    Global Modules
"""
import PyPDF2
from fastapi import UploadFile, HTTPException

"""
    Domain Entities
"""
from src.module.domain.entities.file import File

"""
    External Services
"""
from src.module.infrastructure.external_services.azure_storage.container_client import (
    AzureStorageContainerClient,
)
from src.module.infrastructure.external_services.azure_storage.blob_sas import (
    AzureStorageBlobSas,
)
from src.module.infrastructure.external_services.azure_storage.interfaces.file_interface import (
    AzureStorageFileInterface,
)


class DocumentService:
    def __init__(self):
        self.repository = AzureStorageFileInterface()

    async def get_file_url(self, file_name):
        container_client = AzureStorageContainerClient().client
        # Get the blob client
        blob_client = container_client.container_client.get_blob_client(file_name)
        azure_blob_sas = AzureStorageBlobSas(blob_client)

        # Return the blob URL with the SAS token
        return azure_blob_sas.generate_read_sas()

    async def upload_file(self, file: UploadFile):
        # Create a File class instance from the UploadFile instance
        my_file = File(file)
        # Validate the file
        try:
            await my_file.validate()
            # Upload the file
            blob_client = await self.repository.save(my_file)
            # Return the blob URL
            return {
                "url": await self.repository.get_sas_token_url(blob_client),
                "filename": file.filename,
                "status": "success",
            }
        except ValueError as e:
            # Log the error
            capture_exception(error=e)
            # Raise an HTTPException
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def extract_text_from_pdf(file_path):
        with open(file_path, "rb") as pdf_file_obj:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
            text = "".join(page.extractText() for page in pdf_reader.pages)
        return text
