#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from abc import ABC, abstractmethod


class DocumentProcessingQueue(ABC):
    """
    Schedules the processing of uploaded documents.
    """

    @abstractmethod
    async def enqueue(self, document_id: str) -> None:
        """
        Schedule the processing of a document.
        """

    @abstractmethod
    async def ping(self) -> None:
        """
        Check the queue is reachable. Raises on failure.
        """
