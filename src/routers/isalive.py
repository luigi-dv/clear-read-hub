#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'

from fastapi import Depends

"""
    Global Modules
"""
from typing import Callable
from fastapi.routing import APIRouter

"""
    API Modules
"""
from src.module.application.services.isalive_service import IsAliveService

router = APIRouter()


class IsAlive(Callable):

    def __init__(self, service: IsAliveService = Depends()):
        self.service = service

    @router.get("")
    async def get_is_alive(self):
        result = await self.service.get()
        return result
