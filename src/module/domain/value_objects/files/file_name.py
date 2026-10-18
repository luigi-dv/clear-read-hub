#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import unicodedata

DEFAULT_FILE_NAME = "document"
MAX_FILE_NAME_LENGTH = 255


def sanitize_file_name(name: str | None) -> str:
    """
    Make a client supplied file name safe to store and to echo back in headers.

    Directories are dropped and control characters removed. The name is only used for
    display: files are stored under generated keys.

    :param name: The original file name
    :return: A safe file name
    """
    if not name:
        return DEFAULT_FILE_NAME
    # Keep the last path component, whatever the separator
    name = name.replace("\\", "/").rsplit("/", 1)[-1]
    name = "".join(
        ch
        for ch in unicodedata.normalize("NFC", name)
        if unicodedata.category(ch)[0] != "C"
    )
    name = name.strip().strip(".")
    return name[:MAX_FILE_NAME_LENGTH] or DEFAULT_FILE_NAME
