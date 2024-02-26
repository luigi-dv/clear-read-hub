#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from sentry_sdk import capture_exception
from fastapi import UploadFile, HTTPException

"""
    Domain Modules
"""
from src.module.domain.entities.files.file import File

"""
    Infrastructure Modules
"""
from src.module.infrastructure.services.external.azure.storage.container_client import (
    AzureStorageContainerClient,
)
from src.module.infrastructure.services.external.azure.storage.blob_sas import (
    AzureStorageBlobSas,
)
from src.module.infrastructure.services.external.azure.storage.interfaces.file_interface import (
    AzureStorageFileInterface,
)


class DocumentService:
    """
    Proxy Class for Document Service
    """

    def __init__(self):
        self.repository = AzureStorageFileInterface()

    async def get_file_url(self, file_name):
        container_client = AzureStorageContainerClient().client
        # Get the blob client
        blob_client = container_client.get_blob_client(file_name)
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
