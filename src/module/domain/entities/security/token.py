#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
