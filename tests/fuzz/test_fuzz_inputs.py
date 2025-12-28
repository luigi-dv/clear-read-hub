#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
Property based tests: the code handling untrusted input must never crash with an
unexpected exception, whatever the input.
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from src.module.domain.exceptions import AuthenticationError, TextExtractionError
from src.module.domain.value_objects.files.file_name import (
    MAX_FILE_NAME_LENGTH,
    sanitize_file_name,
)
from src.module.domain.value_objects.files.file_type import FileType
from src.module.infrastructure.security.jwt_token_service import JwtTokenService
from src.module.infrastructure.text_extraction.pymupdf_text_extractor import (
    PyMuPDFTextExtractor,
)
from tests.conftest import TEST_SECRET

token_service = JwtTokenService(TEST_SECRET, "HS256", 15)
extractor = PyMuPDFTextExtractor(max_pages=5)


@given(st.binary(max_size=4096))
def test_sniff_only_returns_allowed_types(content):
    assert FileType.sniff(content) in (None, FileType.PDF, FileType.TXT)


@given(
    st.text(
        alphabet=st.characters(blacklist_categories=["Cc", "Cs"])
        | st.sampled_from("\t\n\r"),
        min_size=1,
        max_size=2048,
    )
)
def test_any_utf8_text_is_text(text):
    content = text.encode("utf-8")
    if not content.startswith(b"%PDF-"):
        assert FileType.sniff(content) == FileType.TXT


@given(st.one_of(st.none(), st.text(max_size=600)))
def test_sanitized_names_are_safe(name):
    sanitized = sanitize_file_name(name)
    assert sanitized
    assert len(sanitized) <= MAX_FILE_NAME_LENGTH
    assert "/" not in sanitized and "\\" not in sanitized
    assert sanitized not in (".", "..")
    assert not any(ord(ch) < 32 or ord(ch) == 127 for ch in sanitized)


@given(st.text(max_size=512))
def test_random_tokens_are_rejected_cleanly(token):
    with pytest.raises(AuthenticationError):
        token_service.verify(token)


@given(st.binary(max_size=2048))
@settings(max_examples=200, deadline=None)
def test_pdf_extraction_never_crashes(content):
    try:
        pages = extractor.extract(b"%PDF-1.7\n" + content, FileType.PDF)
    except TextExtractionError:
        return
    assert all(isinstance(page, str) for page in pages)


@given(st.text(max_size=2048))
def test_txt_extraction_round_trips(text):
    assert extractor.extract(text.encode("utf-8"), FileType.TXT) == [text]
