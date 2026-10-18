#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from abc import ABC, abstractmethod


class IFileStorage(ABC):
    """
    Binary object storage for uploaded files.
    """

    @abstractmethod
    async def initialize(self) -> None:
        """
        Prepare the storage (create the container or directory) at startup.
        """

    @abstractmethod
    async def save(self, key: str, content: bytes, content_type: str) -> None:
        """
        Store the content under the given key, replacing any previous content.
        """

    @abstractmethod
    async def read(self, key: str) -> bytes:
        """
        Read the content stored under the given key.
        :raises StorageObjectNotFoundError: If nothing is stored under the key
        """

    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        Delete the content stored under the given key. Missing keys are ignored.
        """

    @abstractmethod
    async def ping(self) -> None:
        """
        Check the storage is reachable. Raises on failure.
        """
