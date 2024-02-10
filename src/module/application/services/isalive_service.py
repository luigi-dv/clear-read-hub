#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luigelo@ldvloper.com'

from src.module.infrastructure.api_responses.success_response import SuccessResponse


class IsAliveService:
    def __init__(self):
        pass

    async def get(self):
        # Here you can define your logic to check if the service is alive
        return SuccessResponse(message="API is alive", data={})
