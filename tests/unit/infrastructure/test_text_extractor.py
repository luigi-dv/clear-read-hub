#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import pymupdf
import pytest

from src.module.domain.exceptions import TextExtractionError
from src.module.domain.value_objects.files.file_type import FileType
from src.module.infrastructure.text_extraction.pymupdf_text_extractor import (
    PyMuPDFTextExtractor,
)
from tests.conftest import make_pdf


@pytest.fixture
def extractor():
    return PyMuPDFTextExtractor(max_pages=3)


def test_extracts_pdf_pages(extractor):
    pages = extractor.extract(make_pdf(["First page", "Second page"]), FileType.PDF)
    assert len(pages) == 2
    assert "First page" in pages[0]
    assert "Second page" in pages[1]


def test_extracts_text_file(extractor):
    assert extractor.extract("﻿Hola".encode(), FileType.TXT) == ["Hola"]


def test_rejects_corrupt_pdf(extractor):
    with pytest.raises(TextExtractionError):
        extractor.extract(b"%PDF-1.7 this is not really a pdf", FileType.PDF)


def test_rejects_pdf_with_too_many_pages(extractor):
    with pytest.raises(TextExtractionError, match="maximum is 3"):
        extractor.extract(make_pdf(["p"] * 4), FileType.PDF)


def test_rejects_encrypted_pdf(extractor):
    document = pymupdf.open()
    document.new_page().insert_text((72, 72), "secret")
    content = document.tobytes(
        encryption=pymupdf.PDF_ENCRYPT_AES_256, owner_pw="owner", user_pw="user"
    )
    with pytest.raises(TextExtractionError, match="password"):
        extractor.extract(content, FileType.PDF)


def test_rejects_invalid_utf8_text(extractor):
    with pytest.raises(TextExtractionError):
        extractor.extract(b"\xff\xfe", FileType.TXT)
