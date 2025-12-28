#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import pytest

from src.module.domain.exceptions import FileTooLargeError, InvalidInputError
from src.module.domain.value_objects.files.file_name import sanitize_file_name
from src.module.domain.value_objects.files.file_size import FileSize
from src.module.domain.value_objects.files.file_type import FileType


class TestFileType:
    def test_detects_pdf_from_magic_bytes(self):
        assert FileType.sniff(b"%PDF-1.7\n...") == FileType.PDF

    @pytest.mark.parametrize(
        "content",
        [b"Plain text.\n", "Texto en espa\u00f1ol".encode(), b"\xef\xbb\xbfwith BOM"],
    )
    def test_detects_utf8_text(self, content):
        assert FileType.sniff(content) == FileType.TXT

    @pytest.mark.parametrize(
        "content",
        [
            b"",
            b"PK\x03\x04 docx is a zip",
            b"\xd0\xcf\x11\xe0 legacy doc",
            b"text with a \x00 null byte",
            b"PK\x03\x04 control characters",
            b"\xff\xfe\xfd not utf-8",
            b"MZ\x90\x00 executable",
        ],
    )
    def test_rejects_other_content(self, content):
        assert FileType.sniff(content) is None

    def test_allows_whitespace_control_characters(self):
        assert FileType.sniff(b"col1\tcol2\r\nline\x0cfeed") == FileType.TXT

    def test_media_type_and_extension(self):
        assert FileType.PDF.media_type == "application/pdf"
        assert FileType.TXT.extension == ".txt"


class TestFileSize:
    def test_accepts_size_within_limit(self):
        assert FileSize(10, max_size=10).size == 10

    def test_rejects_empty_file(self):
        with pytest.raises(InvalidInputError):
            FileSize(0, max_size=10)

    def test_rejects_too_large_file(self):
        with pytest.raises(FileTooLargeError):
            FileSize(11, max_size=10)


class TestSanitizeFileName:
    @pytest.mark.parametrize(
        ("name", "expected"),
        [
            ("report.pdf", "report.pdf"),
            ("../../etc/passwd", "passwd"),
            ("C:\\Users\\me\\thesis.pdf", "thesis.pdf"),
            ("bad\r\nname.pdf", "badname.pdf"),
            ("..", "document"),
            ("", "document"),
            (None, "document"),
            ("  spaced.txt  ", "spaced.txt"),
        ],
    )
    def test_sanitizes(self, name, expected):
        assert sanitize_file_name(name) == expected

    def test_truncates_long_names(self):
        assert len(sanitize_file_name("a" * 1000 + ".pdf")) == 255
