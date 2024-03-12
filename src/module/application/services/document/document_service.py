#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from sentry_sdk import capture_exception
from fastapi import UploadFile, HTTPException
from src.module.domain.entities.files.file import File
from src.module.infrastructure.services.external.azure.storage.container_client import (
    AzureStorageContainerClient,
)
from src.module.infrastructure.services.external.azure.storage.blob_sas import (
    AzureStorageBlobSas,
)
from src.module.infrastructure.interfaces.files.file_interface import (
    AzureStorageFileInterface,
)


class DocumentService:
    """
    Proxy Class for Document Service
    """

    def __init__(self):
        self.repository = AzureStorageFileInterface()

    @staticmethod
    async def get_document_url(file_name):
        """
        Get the URL of a file from the Azure Storage

        :param file_name: The name of the file
        :return: The URL of the file with the SAS token
        """
        container_client = AzureStorageContainerClient().client
        # Get the blob client
        blob_client = container_client.get_blob_client(file_name)
        azure_blob_sas = AzureStorageBlobSas(blob_client)

        # Return the blob URL with the SAS token
        return azure_blob_sas.generate_read_sas()

    async def upload_file(self, file: UploadFile):
        """
        Upload a file to the Azure Storage

        :param file: The file to upload
        :return: The URL of the uploaded file with the SAS token
        """

        # Create a File class instance from the UploadFile instance
        my_file = File(file)

        try:
            # Validate the file
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
