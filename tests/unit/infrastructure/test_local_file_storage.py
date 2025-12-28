#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import pytest

from src.module.domain.exceptions import StorageObjectNotFoundError
from src.module.infrastructure.storage.local_file_storage import LocalFileStorage


@pytest.fixture
async def local_storage(tmp_path):
    storage = LocalFileStorage(tmp_path / "uploads")
    await storage.initialize()
    return storage


async def test_save_read_delete(local_storage):
    await local_storage.save("user/doc.pdf", b"content", "application/pdf")
    assert await local_storage.read("user/doc.pdf") == b"content"
    await local_storage.delete("user/doc.pdf")
    with pytest.raises(StorageObjectNotFoundError):
        await local_storage.read("user/doc.pdf")


async def test_save_replaces_content(local_storage):
    await local_storage.save("k", b"one", "text/plain")
    await local_storage.save("k", b"two", "text/plain")
    assert await local_storage.read("k") == b"two"


async def test_delete_missing_key_is_ignored(local_storage):
    await local_storage.delete("missing")


async def test_no_temporary_files_are_left(local_storage):
    await local_storage.save("user/doc.txt", b"x", "text/plain")
    assert [p.name for p in (local_storage.base_path / "user").iterdir()] == ["doc.txt"]


@pytest.mark.parametrize("key", ["../escape", "/etc/passwd", "a/../../b", "", "."])
async def test_rejects_keys_outside_base_path(local_storage, key):
    with pytest.raises(ValueError):
        await local_storage.save(key, b"x", "text/plain")


async def test_ping(local_storage):
    await local_storage.ping()
