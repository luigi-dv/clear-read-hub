#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from src.module.infrastructure.persistence.db_context import DatabaseContext
from src.module.domain.entities.oauth.user import User


class UserRepository:
    def __init__(self):
        self.context = DatabaseContext()
        self.database = self.context.get_database()  # 'users' collection
        self.collection = self.database.users

    async def create_user(self, user: User) -> User:
        """
        Create the user
        :param user:
        :return:
        """
        result = self.collection.insert_one(user.dict(by_alias=True))
        user.id = result.inserted_id
        return user

    async def get_user(self, username: str) -> User:
        """
        Get the user by username
        :param username:
        :return:
        """
        document = self.collection.find_one({"username": username})
        return User(**document) if document else None

    async def get_user_by_id(self, user_id: str) -> User:
        """
        Get the user by id
        :param user_id:
        :return:
        """
        document = self.collection.find_one({"_id": user_id})
        return User(**document) if document else None

    async def update_user(self, user: User) -> User:
        """
        Update the user
        :param user:
        :return:
        """
        self.collection.update_one({"_id": user.id}, {"$set": user.dict(by_alias=True)})
        return user

    async def delete_user(self, user_id: str) -> bool:
        """
        Delete the user
        :param user_id:
        :return:
        """
        result = self.collection.delete_one({"_id": user_id})
        return result.deleted_count > 0
