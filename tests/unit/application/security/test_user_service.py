#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from src.module.application.services.security.user_service import UserService
from src.module.domain.entities.security.user import User


async def test_create_user():
    """
    Test Create User
    """
    service = UserService()
    user = User(username="testuser", hashed_password="testpassword", disabled=False)
    created_user = await service.create_user(user)
    assert created_user.username == "testuser"
    assert created_user.hashed_password == "testpassword"
    assert created_user.disabled == False


async def test_get_user():
    """
    Test Get User
    """
    service = UserService()
    # Test get_user method
    fetched_user = await service.get_user("testuser")
    assert fetched_user.username == "testuser"


async def test_update_user():
    """
    Test Update User
    """
    service = UserService()
    updated_user = await service.update_user(
        User(username="testuser", hashed_password="newpassword", disabled=True)
    )
    assert updated_user.hashed_password == "newpassword"
    assert updated_user.disabled == True


async def test_delete_user():
    """
    Test Delete User
    """
    service = UserService()
    assert service.delete_user("testuser") == True
