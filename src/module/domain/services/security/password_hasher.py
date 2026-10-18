#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """
    Password Hasher Interface
    """

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        pass
