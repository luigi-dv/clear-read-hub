#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'

"""
 Global Modules
"""
from azure.storage.blob import BlobServiceClient, BlobClient


class AzureStorageFileUploader:
    def __init__(self, connection_string):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def upload_file(self, file_content, container_name, blob_name) -> BlobClient:
        # Create a blob client using the local file name as the name for the blob
        blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
        # Upload the file content
        blob_client.upload_blob(file_content)
        # Return the blob
        return blob_client
