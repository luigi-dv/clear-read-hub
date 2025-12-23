#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import pymupdf

from src.module.domain.exceptions import TextExtractionError
from src.module.domain.services.documents.text_extractor import TextExtractor
from src.module.domain.value_objects.files.file_type import FileType


class PyMuPDFTextExtractor(TextExtractor):
    """
    Extracts text from PDF files with PyMuPDF, and decodes plain text files.
    """

    def __init__(self, max_pages: int):
        self.max_pages = max_pages

    def extract(self, content: bytes, file_type: FileType) -> list[str]:
        if file_type == FileType.PDF:
            return self._extract_pdf(content)
        if file_type == FileType.TXT:
            return self._extract_txt(content)
        raise TextExtractionError(f"Unsupported file type: {file_type}")

    def _extract_pdf(self, content: bytes) -> list[str]:
        try:
            document = pymupdf.open(stream=content, filetype="pdf")
        except Exception as e:
            raise TextExtractionError("The PDF file is corrupt or unreadable.") from e

        with document:
            if document.needs_pass:
                raise TextExtractionError("The PDF file is password protected.")
            if document.page_count > self.max_pages:
                raise TextExtractionError(
                    f"The PDF has {document.page_count} pages, "
                    f"the maximum is {self.max_pages}."
                )
            try:
                # sort=True returns text in natural reading order
                return [page.get_text("text", sort=True) for page in document]
            except Exception as e:
                raise TextExtractionError("The PDF content could not be read.") from e

    @staticmethod
    def _extract_txt(content: bytes) -> list[str]:
        try:
            return [content.decode("utf-8-sig")]
        except UnicodeDecodeError as e:
            raise TextExtractionError("The text file is not valid UTF-8.") from e
