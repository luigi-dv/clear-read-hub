#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'

from src.module.infrastructure.external_services.azure_storage.blob_sas import AzureStorageBlobSas

"""
    Global Modules
"""
import PyPDF2
from fastapi import UploadFile, File


"""
    Core Settings
"""
from src.core.settings import coresettings


"""
    External Services
"""
from src.module.infrastructure.external_services.azure_storage.file_uploader import AzureStorageFileUploader
from src.module.infrastructure.external_services.azure_storage.container_client import AzureStorageContainerClient


class DocumentService:
    def __init__(self,
                 account_name=coresettings.AZ_STORAGE_ACCOUNT_NAME,
                 account_key=coresettings.AZ_STORAGE_ACCOUNT_KEY,
                 connection_string=coresettings.AZ_STORAGE_CONNECTION_STRING,
                 container_name=coresettings.AZ_STORAGE_CONTAINER_NAME):
        self.account_name = account_name
        self.account_key = account_key
        self.connection_string = connection_string
        self.container_name = container_name
        self.uploader = AzureStorageFileUploader(connection_string)

    async def get_file_url(self, file_name):
        container_client = AzureStorageContainerClient(self.connection_string, self.container_name)
        # Get the blob client
        blob_client = container_client.container_client.get_blob_client(file_name)
        # Create a new instance of the AzureStorageBlobSas class
        print("account key:" + self.account_key)
        azure_blob_sas = AzureStorageBlobSas(blob_client, self.account_key)

        # Return the blob URL with the SAS token
        return azure_blob_sas.generate_read_sas()

    async def upload_file(self, file: UploadFile = File(...)):
        # Upload the file
        container_client = AzureStorageContainerClient(self.connection_string, self.container_name)
        blob_url = self.uploader.upload_file(await file.read(), container_client.container_name, file.filename)
        # Return the blob URL
        return {"url": blob_url, "filename": file.filename, "status": "success"}

    @staticmethod
    def extract_text_from_pdf(file_path):
        with open(file_path, 'rb') as pdf_file_obj:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
            text = ''.join(page.extractText() for page in pdf_reader.pages)
        return text

