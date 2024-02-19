#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"


from src.module.domain.entities.security.user import User


def test_user_model():
    user = User(username="testuser", hashed_password="testpassword", disabled=False)
    assert user.username == "testuser"
    assert user.hashed_password == "testpassword"
    assert user.disabled == False
