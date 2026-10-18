#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import asyncio

from src.module.domain.entities.security.token import Token
from src.module.domain.entities.security.user import User
from src.module.domain.exceptions import AuthenticationError, NotFoundError
from src.module.domain.repositories.security.user_repository import IUserRepository
from src.module.domain.services.security.password_hasher import PasswordHasher
from src.module.domain.services.security.token_service import TokenService


class UserService:
    """
    User Service

    This class is responsible for handling the user business logic and operations.
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service
        self._dummy_hash: str | None = None

    async def register(self, email: str, password: str) -> User:
        """
        Create a new user

        :param email: The user email
        :param password: The plain password
        :return: The created user
        :raises ConflictError: If the email is already registered
        """
        hashed_password = await self._hash(password)
        user = User(email=_normalize_email(email), hashed_password=hashed_password)
        return await self.user_repository.create(user)

    async def get_user(self, user_id: str) -> User:
        """
        Get the user by id

        :param user_id: The user id
        :return: The user
        :raises NotFoundError: If the user does not exist
        """
        user = await self.user_repository.find_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found.")
        return user

    async def update_user(
        self,
        user: User,
        current_password: str | None,
        email: str | None = None,
        password: str | None = None,
    ) -> User:
        """
        Update the email and/or the password of a user.

        Changing the password requires the current password.

        :return: The updated user
        """
        if password is not None:
            if current_password is None or not await self._verify(
                current_password, user.hashed_password
            ):
                raise AuthenticationError("The current password is not correct.")
            user.hashed_password = await self._hash(password)
        if email is not None:
            user.email = _normalize_email(email)
        user.touch()
        return await self.user_repository.update(user)

    async def delete_user(self, user_id: str) -> None:
        """
        Delete the user

        :param user_id: The user id
        """
        if not await self.user_repository.delete(user_id):
            raise NotFoundError("User not found.")

    async def authenticate(self, email: str, password: str) -> Token:
        """
        Check the credentials of a user and issue an access token.

        :param email: The user email
        :param password: The user password
        :return: The access token
        :raises AuthenticationError: If the credentials are not valid
        """
        user = await self.user_repository.find_by_email(_normalize_email(email))
        if user is None:
            # Hash anyway so response times do not reveal which emails exist
            await self._verify(password, await self._get_dummy_hash())
            raise AuthenticationError("Incorrect email or password.")
        if not await self._verify(password, user.hashed_password):
            raise AuthenticationError("Incorrect email or password.")
        if user.disabled:
            raise AuthenticationError("The user is disabled.")
        return self.token_service.issue(user.id)

    async def get_current_user(self, token: str) -> User:
        """
        Get the user an access token was issued for.

        :param token: The access token
        :return: The user
        :raises AuthenticationError: If the token or the user are not valid
        """
        user_id = self.token_service.verify(token)
        user = await self.user_repository.find_by_id(user_id)
        if user is None or user.disabled:
            raise AuthenticationError()
        return user

    # bcrypt is CPU bound on purpose: keep it off the event loop
    async def _hash(self, password: str) -> str:
        return await asyncio.to_thread(self.password_hasher.hash_password, password)

    async def _verify(self, password: str, hashed_password: str) -> bool:
        return await asyncio.to_thread(
            self.password_hasher.verify_password, password, hashed_password
        )

    async def _get_dummy_hash(self) -> str:
        if self._dummy_hash is None:
            self._dummy_hash = await self._hash("dummy-password-for-timing")
        return self._dummy_hash


def _normalize_email(email: str) -> str:
    return email.strip().lower()
