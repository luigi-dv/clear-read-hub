#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
    Global Modules
"""
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException

"""
    API Modules
"""
from src.module.domain.entities.security.user import User
from src.module.application.services.security.user_service import UserService


class Users:
    """
    Class Proxy Users
    """

    def __init__(self):
        self.router = APIRouter()
        self.get_customized_router()  # Add routes to the router

    @staticmethod
    def get_router():
        users = Users()
        return users.router

    def get_customized_router(self):
        """
        Customized router for Users.
        """

        @self.router.post("/", response_model=User)
        async def create_user(user: User, service: UserService = Depends()):
            """
            Create a new user
            """
            return await service.create_user(user)

        @self.router.get("/{username}", response_model=User)
        async def read_user(username: str, service: UserService = Depends()):
            """
            Get a specific user by username
            """
            return await service.get_user(username)

        @self.router.get("/id/{user_id}", response_model=User)
        async def read_user_by_id(user_id: str, service: UserService = Depends()):
            """
            Get a specific user by user_id
            """
            return await service.get_user_by_id(user_id)

        @self.router.put("/", response_model=User)
        async def update_user(
            user: User,
            current_user: User = Depends(UserService.get_current_user),
            service: UserService = Depends(),
        ):
            """
            Update an existing user
            """
            if user.username != current_user.username:
                raise HTTPException(status_code=400, detail="Not enough permissions")
            return await service.update_user(user)

        @self.router.delete("/{user_id}")
        async def delete_user(
            user_id: str,
            current_user: User = Depends(UserService.get_current_user),
            service: UserService = Depends(),
        ):
            """
            Delete a user
            """
            if user_id != current_user.id:
                raise HTTPException(status_code=400, detail="Not enough permissions")
            return await service.delete_user(user_id)
