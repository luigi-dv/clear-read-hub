#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from abc import ABC, abstractmethod
from src.module.domain.entities.security.user import User


class IUserRepository(ABC):

    @abstractmethod
    async def find_by_id(self, user_id: str) -> User:
        """
        Find a user by its id
        :param user_id: The user id
        :return: The user
        """
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> User:
        """
        Find a user by its email
        :param email: The user email
        :return: The user
        """
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Create a new user
        :param user: The user to create
        :return: The created user
        """
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """
        Update a user
        :param user: The user to update
        :return: The updated user
        """
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """
        Delete a user
        :param user_id: The user id
        :return:
        """
        pass
