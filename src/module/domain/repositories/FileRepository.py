#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'

from abc import ABC, abstractmethod
from azure.storage.blob import BlobClient

"""
    Domain Modules
"""
from src.module.domain.entities.File import File


class FileRepository(ABC):
    @abstractmethod
    async def save(self, file: File) -> BlobClient:
        pass

    @abstractmethod
    async def get_sas_token_url(self, blob_client: BlobClient) -> str:
        pass
