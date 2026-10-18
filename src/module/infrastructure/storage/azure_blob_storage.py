#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import asyncio

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, ContentSettings

from src.module.domain.exceptions import StorageObjectNotFoundError
from src.module.domain.repositories.files.file_storage import IFileStorage


class AzureBlobStorage(IFileStorage):
    """
    Stores files as blobs in an Azure Storage container (or Azurite locally).

    Blobs stay private: clients download them through the API, which checks ownership.
    """

    def __init__(self, connection_string: str, container_name: str):
        self.service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container = self.service_client.get_container_client(container_name)

    async def initialize(self) -> None:
        try:
            await asyncio.to_thread(self.container.create_container)
        except ResourceExistsError:
            pass

    async def save(self, key: str, content: bytes, content_type: str) -> None:
        await asyncio.to_thread(
            self.container.upload_blob,
            name=key,
            data=content,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type),
        )

    async def read(self, key: str) -> bytes:
        def _download() -> bytes:
            return self.container.download_blob(key).readall()

        try:
            return await asyncio.to_thread(_download)
        except ResourceNotFoundError as e:
            raise StorageObjectNotFoundError() from e

    async def delete(self, key: str) -> None:
        try:
            await asyncio.to_thread(self.container.delete_blob, key)
        except ResourceNotFoundError:
            pass

    async def ping(self) -> None:
        await asyncio.to_thread(self.container.get_container_properties)

    def close(self) -> None:
        self.service_client.close()
