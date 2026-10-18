#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from enum import StrEnum

# Bytes inspected to decide whether a file is plain text.
_TEXT_SNIFF_BYTES = 8192
# Control characters never found in text files, but common in binary formats
_BINARY_CONTROL_CHARS = frozenset(
    chr(c) for c in [*range(0x00, 0x09), 0x0B, *range(0x0E, 0x20), 0x7F]
)


class FileType(StrEnum):
    """
    File types the platform accepts. Only types we can extract text from are allowed.
    """

    PDF = "pdf"
    TXT = "txt"

    @property
    def media_type(self) -> str:
        return {
            FileType.PDF: "application/pdf",
            FileType.TXT: "text/plain; charset=utf-8",
        }[self]

    @property
    def extension(self) -> str:
        return f".{self.value}"

    @classmethod
    def sniff(cls, content: bytes) -> "FileType | None":
        """
        Detect the file type from its content instead of trusting the client headers.

        :param content: The file content
        :return: The detected file type, or None if the type is not allowed
        """
        if content.startswith(b"%PDF-"):
            return cls.PDF
        if _looks_like_text(content):
            return cls.TXT
        return None


def _looks_like_text(content: bytes) -> bool:
    if not content:
        return False
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        return False
    return _BINARY_CONTROL_CHARS.isdisjoint(text[:_TEXT_SNIFF_BYTES])
