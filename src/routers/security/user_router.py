#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
    Global Modules
"""
from fastapi import Response, status
from fastapi.routing import APIRouter

"""
    API Modules
"""
from src.module.infrastructure.serializers.security.user_schemas import (
    UserCreate,
    UserPublic,
    UserUpdate,
)
from src.routers.dependencies import CurrentUser, DocumentServiceDep, UserServiceDep


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

        @self.router.post(
            "", response_model=UserPublic, status_code=status.HTTP_201_CREATED
        )
        async def create_user(user: UserCreate, service: UserServiceDep):
            """
            Register a new user.

            Raises:
            - `409`: If the email is already registered.
            """
            return await service.register(user.email, user.password)

        @self.router.get("/me", response_model=UserPublic)
        async def read_current_user(current_user: CurrentUser):
            """
            Get the authenticated user.
            """
            return current_user

        @self.router.patch("/me", response_model=UserPublic)
        async def update_current_user(
            changes: UserUpdate, current_user: CurrentUser, service: UserServiceDep
        ):
            """
            Update the email and/or password of the authenticated user.

            Changing the password requires `current_password`.
            """
            return await service.update_user(
                current_user,
                current_password=changes.current_password,
                email=changes.email,
                password=changes.password,
            )

        @self.router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_current_user(
            current_user: CurrentUser,
            service: UserServiceDep,
            documents: DocumentServiceDep,
        ):
            """
            Delete the authenticated user and all of their documents.
            """
            await documents.delete_all_documents(current_user.id)
            await service.delete_user(current_user.id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
