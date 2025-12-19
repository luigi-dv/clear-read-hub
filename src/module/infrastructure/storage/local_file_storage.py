#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import asyncio
import os
import tempfile
from pathlib import Path

from src.module.domain.exceptions import StorageObjectNotFoundError
from src.module.domain.repositories.files.file_storage import IFileStorage


class LocalFileStorage(IFileStorage):
    """
    Stores files in a local directory. Used for development and single node setups.
    """

    def __init__(self, base_path: str | Path):
        self.base_path = Path(base_path).resolve()

    async def initialize(self) -> None:
        await asyncio.to_thread(self.base_path.mkdir, parents=True, exist_ok=True)

    async def save(self, key: str, content: bytes, content_type: str) -> None:
        await asyncio.to_thread(self._write, self._path(key), content)

    async def read(self, key: str) -> bytes:
        try:
            return await asyncio.to_thread(self._path(key).read_bytes)
        except FileNotFoundError as e:
            raise StorageObjectNotFoundError() from e

    async def delete(self, key: str) -> None:
        await asyncio.to_thread(self._path(key).unlink, missing_ok=True)

    async def ping(self) -> None:
        if not os.access(self.base_path, os.W_OK):
            raise OSError(f"Storage path {self.base_path} is not writable")

    def _path(self, key: str) -> Path:
        path = (self.base_path / key).resolve()
        # Never read or write outside the storage directory
        if not path.is_relative_to(self.base_path) or path == self.base_path:
            raise ValueError(f"Invalid storage key: {key!r}")
        return path

    @staticmethod
    def _write(path: Path, content: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write to a temporary file first, so readers never see half written files
        fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=".upload-")
        try:
            with os.fdopen(fd, "wb") as tmp:
                tmp.write(content)
            os.replace(tmp_name, path)
        except BaseException:
            Path(tmp_name).unlink(missing_ok=True)
            raise
