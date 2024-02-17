#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from src.module.application.services.oauth.token_service import TokenService

"""
    Global Modules
"""
from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

"""
    API Modules
"""
from src.module.domain.entities.oauth.token import Token
from src.module.domain.entities.oauth.user import User
from src.module.application.services.user_service import UserService


class OAuth:
    """
    Class proxy OAuth
    """

    def __init__(self):
        self.router = APIRouter()
        self.get_customized_router()  # Add routes to the router

    @staticmethod
    def get_router():
        oauth = OAuth()
        return oauth.router

    def get_customized_router(self):
        """
        Customized router for OAuth.
        :return:
        """

        @self.router.post("/token")
        async def login_for_access_token(
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
        ) -> Token:
            """
            Login for access token
            :param form_data:
            :return:
            """

            user = await UserService.authenticate_user(
                form_data.username, form_data.password
            )
            return TokenService.login_for_access_token(user)

        @self.router.get("/users/me/", response_model=User)
        async def read_users_me(
            current_user: Annotated[User, Depends(UserService.get_current_user)]
        ):
            """
            Read users me
            :param current_user:
            :return:
            """
            return current_user
