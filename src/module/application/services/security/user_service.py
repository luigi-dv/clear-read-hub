#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from typing import Annotated
from jose import JWTError, jwt

from src.module.infrastructure.utilities.hashing.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from src.service_config import serviceConfig
from fastapi import Depends, HTTPException, status
from src.module.infrastructure.configuration.security import oauth2_scheme
from src.module.domain.entities.security.user import User
from src.module.domain.entities.security.token_data import TokenData
from src.module.infrastructure.interfaces.security.user_repository import UserRepository
from src.module.infrastructure.utilities.hashing.password import verify_password


class UserService:
    """
    User Service

    This class is responsible for handling the user business logic and operations.
    """

    def __init__(self):
        self.user_repository = UserRepository()

    async def get_user(self, email: str) -> User:
        """
        Get the user by email

        :param email: The user email
        :return: The user
        """
        user = await self.user_repository.find_by_email(email)
        return user

    async def get_user_by_id(self, user_id: str) -> User:
        """
        Get the user by id

        :param user_id: The user id
        :return: The user
        """
        user = await self.user_repository.find_by_id(user_id)
        return user

    async def create_user(self, user: User) -> User:
        """
        Create the user

        :param user: The user to create
        :return: The created user
        """
        password_hasher = BcryptPasswordHasher()
        user.password = password_hasher.hash_password(user.password)
        user = await self.user_repository.create(user)
        return user

    async def update_user(self, user: User) -> User:
        """
        Update the user

        :param user: User to update
        :return: The updated user
        """
        user = await self.user_repository.update(user)
        return user

    async def delete_user(self, user_id: str) -> bool:
        """
        Delete the user

        :param user_id: The user id
        :return: The result of the operation
        """
        result = await self.user_repository.delete(user_id)
        return result

    @staticmethod
    async def authenticate_user(email: str, password: str):
        """
        Authenticate the user

        :param email: The user email
        :param password: The user password
        :return: The user
        """
        user = await UserService().get_user(email=email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        """
        Get the current user from the token

        :param token: The token
        :return: The user
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                serviceConfig.SERVICE_OAUTH_CLIENT_SECRET,
                algorithms=[serviceConfig.SERVICE_OAUTH_ENCODE_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(email=username)
        except JWTError:
            raise credentials_exception
        user = UserService().get_user(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user
