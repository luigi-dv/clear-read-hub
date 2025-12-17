#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from src.module.domain.exceptions import FileTooLargeError, InvalidInputError


class FileSize:
    def __init__(self, size: int, max_size: int):
        if size <= 0:
            raise InvalidInputError("The file is empty.")
        if size > max_size:
            raise FileTooLargeError(
                f"File size exceeds the maximum limit of {max_size} bytes."
            )
        self.size = size
