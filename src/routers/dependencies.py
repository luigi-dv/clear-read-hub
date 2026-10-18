#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from src.module.application.services.document.document_service import DocumentService
from src.module.application.services.security.user_service import UserService
from src.module.domain.entities.security.user import User
from src.module.infrastructure.container import Container

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth2/token")


def get_container(request: Request) -> Container:
    return request.app.state.container


def get_user_service(
    container: Annotated[Container, Depends(get_container)],
) -> UserService:
    return UserService(
        container.user_repository, container.password_hasher, container.token_service
    )


def get_document_service(
    container: Annotated[Container, Depends(get_container)],
) -> DocumentService:
    return DocumentService(
        container.document_repository,
        container.storage,
        container.queue,
        container.settings.MAX_UPLOAD_BYTES,
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    return await service.get_current_user(token)


CurrentUser = Annotated[User, Depends(get_current_user)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
DocumentServiceDep = Annotated[DocumentService, Depends(get_document_service)]
