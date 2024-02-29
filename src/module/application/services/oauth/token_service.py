#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from starlette import status
from datetime import timedelta
from fastapi import HTTPException
from src.module.domain.entities.security.token import Token
from src.module.domain.entities.security.user import User
from src.service_config import serviceConfig
from src.module.infrastructure.utilities.jwt.access_token import create_access_token


class TokenService:
    """
    Proxy Class for Token Service
    """

    def __init__(self):
        pass

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta) -> str:
        """
        Create the access token

        :param data: The data to encode in the token
        :param expires_delta: The expiration time
        :return: The access token
        """
        return create_access_token(data, expires_delta)

    @staticmethod
    def login_for_access_token(user: User) -> Token:
        """
        Login for access token
        :param user: The user
        :return: The access token
        """
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(
            minutes=int(serviceConfig.SERVICE_OAUTH_EXPIRES_IN)
        )
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
