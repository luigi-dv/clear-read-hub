#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"


class DomainError(Exception):
    """
    Base class for every error raised by the domain and application layers.

    The API layer maps each subclass to an HTTP status code, so the inner layers
    never depend on FastAPI.
    """

    default_message = "The operation failed."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class NotFoundError(DomainError):
    default_message = "Resource not found."


class ConflictError(DomainError):
    default_message = "The operation conflicts with the current state."


class AuthenticationError(DomainError):
    default_message = "Could not validate credentials."


class PermissionDeniedError(DomainError):
    default_message = "Not enough permissions."


class InvalidInputError(DomainError):
    default_message = "The provided data is invalid."


class FileTooLargeError(InvalidInputError):
    default_message = "File size exceeds the maximum limit."


class UnsupportedFileTypeError(InvalidInputError):
    default_message = "File type not allowed."


class DocumentNotReadyError(ConflictError):
    default_message = "The document has not been processed yet."


class StorageObjectNotFoundError(NotFoundError):
    default_message = "Stored file not found."


class TextExtractionError(DomainError):
    """
    The document content cannot be extracted (corrupt, encrypted, too many pages).

    This is a permanent failure: retrying the same input will fail again.
    """

    default_message = "Text could not be extracted from the document."
