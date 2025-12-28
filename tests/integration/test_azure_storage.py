#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import pytest

from src.module.domain.exceptions import StorageObjectNotFoundError
from src.module.infrastructure.storage.azure_blob_storage import AzureBlobStorage

pytestmark = pytest.mark.integration


@pytest.fixture
async def azure_storage(azure_connection_string, unique_name):
    storage = AzureBlobStorage(azure_connection_string, unique_name)
    await storage.initialize()
    # Initializing twice must not fail
    await storage.initialize()
    yield storage
    storage.container.delete_container()
    storage.close()


async def test_save_read_delete(azure_storage):
    await azure_storage.ping()
    await azure_storage.save("user/doc.pdf", b"%PDF-content", "application/pdf")
    assert await azure_storage.read("user/doc.pdf") == b"%PDF-content"
    properties = azure_storage.container.get_blob_client("user/doc.pdf")
    assert (
        properties.get_blob_properties().content_settings.content_type
        == "application/pdf"
    )

    await azure_storage.delete("user/doc.pdf")
    await azure_storage.delete("user/doc.pdf")
    with pytest.raises(StorageObjectNotFoundError):
        await azure_storage.read("user/doc.pdf")


async def test_save_overwrites(azure_storage):
    await azure_storage.save("k", b"one", "text/plain")
    await azure_storage.save("k", b"two", "text/plain")
    assert await azure_storage.read("k") == b"two"
