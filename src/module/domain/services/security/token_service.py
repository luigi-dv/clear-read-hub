#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from abc import ABC, abstractmethod

from src.module.domain.entities.security.token import Token


class TokenService(ABC):
    """
    Issues and verifies access tokens.
    """

    @abstractmethod
    def issue(self, subject: str) -> Token:
        """
        Issue an access token for the subject (the user id).
        """

    @abstractmethod
    def verify(self, token: str) -> str:
        """
        Verify an access token.
        :return: The subject of the token
        :raises AuthenticationError: If the token is invalid or expired
        """
