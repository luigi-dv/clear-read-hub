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
        self.set_customized_router()  # Add routes to the router

    @staticmethod
    def get_router():
        users = Users()
        return users.router

    def set_customized_router(self):
        """
        Customized router for Users.
        """

        @self.router.post("/", response_model=User)
        async def create_user(user: User, service: UserService = Depends()):
            """
            Create a new user.

            Parameters:
            - `user` (User): The user details to be created.

            Returns:
            - `User`: The created user details.

            Raises:
            - `HTTPException`: If the user creation fails.
            """

            return await service.create_user(user)

        @self.router.get("/{username}", response_model=User)
        async def read_user(username: str, service: UserService = Depends()):
            """
            Get a specific user by username.

            Parameters:
            - `username` (str): The username of the user to retrieve.

            Returns:
            - `User`: The user details.

            Raises:
            - `HTTPException`: If the user is not found.
            """

            return await service.get_user(username)

        @self.router.get("/id/{user_id}", response_model=User)
        async def read_user_by_id(user_id: str, service: UserService = Depends()):
            """
            Get a specific user by user_id.

            Parameters:
            - `user_id` (str): The user_id of the user to retrieve.

            Returns:
            - `User`: The user details.

            Raises:
            - `HTTPException`: If the user is not found.
            """

            return await service.get_user_by_id(user_id)

        @self.router.put("/", response_model=User)
        async def update_user(
            user: User,
            current_user: User = Depends(UserService.get_current_user),
            service: UserService = Depends(),
        ):
            """
            Update an existing user.

            Parameters:
            - `user` (User): The updated user details.
            - `current_user` (User): The currently authenticated user.

            Returns:
            - `User`: The updated user details.

            Raises:
            - `HTTPException`: If the update fails or if the user making the request doesn't have enough permissions.
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
            Delete a user.

            Parameters:
            - `user_id` (str): The user_id of the user to delete.
            - `current_user` (User): The currently authenticated user.

            Returns:
            - `Dict[str, str]`: A dictionary with a success message.

            Raises:
            - `HTTPException`: If the deletion fails or if the user making the request doesn't have enough permissions.
            """

            if user_id != current_user.id:
                raise HTTPException(status_code=400, detail="Not enough permissions")
            return await service.delete_user(user_id)
