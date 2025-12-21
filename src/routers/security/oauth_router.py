#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"


"""
    Global Modules
"""
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

"""
    API Modules
"""
from src.module.domain.entities.security.token import Token
from src.routers.dependencies import UserServiceDep


class OAuth:
    """
    Class proxy OAuth
    """

    def __init__(self):
        self.router = APIRouter()
        self.set_customized_router()  # Add routes to the router

    @staticmethod
    def get_router():
        oauth = OAuth()
        return oauth.router

    def set_customized_router(self):
        """
        Customized router for OAuth.
        """

        @self.router.post("/token")
        async def login_for_access_token(
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
            service: UserServiceDep,
        ) -> Token:
            """
            Exchange an email (sent as `username`) and a password for an access token.
            """
            return await service.authenticate(form_data.username, form_data.password)
