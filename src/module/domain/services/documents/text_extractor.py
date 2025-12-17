#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from abc import ABC, abstractmethod

from src.module.domain.value_objects.files.file_type import FileType


class TextExtractor(ABC):

    @abstractmethod
    def extract(self, content: bytes, file_type: FileType) -> list[str]:
        """
        Extract the text of a file.

        :return: The text of each page
        :raises TextExtractionError: If the content cannot be read
        """
