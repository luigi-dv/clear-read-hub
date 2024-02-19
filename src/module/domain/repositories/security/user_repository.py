#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"


from fastapi import HTTPException
from src.module.infrastructure.persistence.db_context import DatabaseContext
from src.module.domain.entities.security.user import User
from src.module.infrastructure.configuration.files_loader import load_responses


class UserRepository:
    def __init__(self):
        self.context = DatabaseContext()
        self.database = self.context.get_database()  # 'users' collection
        self.collection = self.database.users
        self.responses = load_responses()

    async def create_user(self, user: User) -> User:
        result = self.collection.insert_one(user.dict(by_alias=True))
        if result.acknowledged:
            user.id = result.inserted_id
            return user
        else:
            raise HTTPException(
                status_code=500, detail=self.responses.module.domain.operation_failed
            )

    async def get_user(self, username: str) -> User:
        document = self.collection.find_one({"username": username})
        if document:
            return User(**document)
        else:
            raise HTTPException(
                status_code=404,
                detail=self.responses.module.domain.error.operation_failed,
            )

    async def get_user_by_id(self, user_id: str) -> User:
        document = self.collection.find_one({"_id": user_id})
        if document:
            return User(**document)
        else:
            raise HTTPException(
                status_code=404,
                detail=self.responses.module.domain.error.operation_failed,
            )

    async def update_user(self, user: User) -> User:
        result = self.collection.update_one(
            {"_id": user.id}, {"$set": user.dict(by_alias=True)}
        )
        if result.modified_count > 0:
            return user
        else:
            raise HTTPException(
                status_code=404, detail="User not found or not modified"
            )

    async def delete_user(self, user_id: str) -> bool:
        result = self.collection.delete_one({"_id": user_id})
        if result.deleted_count > 0:
            return True
        else:
            raise HTTPException(status_code=404, detail="User not found or not deleted")
