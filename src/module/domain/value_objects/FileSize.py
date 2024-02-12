#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'


class FileSize:
    def __init__(self, size: int, MAX_FILE_SIZE=2040):
        if size > MAX_FILE_SIZE:
            raise ValueError("File size exceeds the maximum limit")
        self.size = size
