#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'


class FileType:
    def __init__(self, extension: str):
        if extension not in ["pdf", "docx", "doc", "txt", "rtf", "odt"]:
            raise ValueError("File type not allowed")
        self.extension = extension
