#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import bcrypt

from src.module.domain.services.security.password_hasher import PasswordHasher

# bcrypt only uses the first 72 bytes of a password; longer ones are rejected upstream
MAX_PASSWORD_BYTES = 72


class BcryptPasswordHasher(PasswordHasher):
    """
    Bcrypt Password Hasher
    """

    def __init__(self, rounds: int = 12):
        self.rounds = rounds

    def hash_password(self, password: str) -> str:
        """
        Hash the password

        :param password: The password
        :return: The hashed password
        """
        salt = bcrypt.gensalt(rounds=self.rounds)
        return bcrypt.hashpw(_encode(password), salt).decode("ascii")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Check a password against a hash

        :param password: The password
        :param hashed_password: The stored hash
        :return: True if the password matches
        """
        try:
            return bcrypt.checkpw(_encode(password), hashed_password.encode("ascii"))
        except ValueError:
            return False


def _encode(password: str) -> bytes:
    encoded = password.encode("utf-8")
    if len(encoded) > MAX_PASSWORD_BYTES:
        raise ValueError(f"Passwords are limited to {MAX_PASSWORD_BYTES} bytes")
    return encoded
