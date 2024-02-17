"""
    Global Modules
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


"""
    Configuration Modules
"""
from src.service_config import serviceConfig
from src.module.infrastructure.configuration.security import oauth2_scheme

"""
    Domain Modules
"""
from src.module.domain.entities.oauth.user import User
from src.module.domain.entities.oauth.token_data import TokenData
from src.module.domain.repositories.oauth.user_repository import UserRepository

"""
    Infrastructure Modules
"""
from src.module.infrastructure.utilities.hashing.password import verify_password


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    # User CRUD
    async def create_user(self, user: User) -> User:
        """
        Create the user
        :param user:
        :return:
        """
        user = await self.user_repository.create_user(user)
        return user

    async def get_user(self, username: str) -> User:
        """
        Get the user by username
        :param username:
        :return:
        """
        user = await self.user_repository.get_user(username)
        return user

    async def get_user_by_id(self, user_id: str) -> User:
        """
        Get the user by id
        :param user_id:
        :return:
        """
        user = await self.user_repository.get_user_by_id(user_id)
        return user

    async def update_user(self, user: User) -> User:
        """
        Update the user
        :param user:
        :return:
        """
        user = await self.user_repository.update_user(user)
        return user

    async def delete_user(self, user_id: str) -> bool:
        """
        Delete the user
        :param user_id:
        :return:
        """
        result = await self.user_repository.delete_user(user_id)
        return result

    @staticmethod
    async def authenticate_user(username: str, password: str):
        """
        Authenticate the user
        :param username:
        :param password:
        :return:
        """
        user = await UserService.get_user(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        """
        Get the current user from the token
        :param token:
        :return:
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
                algorithms=[serviceConfig.SERVICE_OAUTH_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = UserService.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
