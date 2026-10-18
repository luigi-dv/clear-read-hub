#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import asyncio
import logging
from typing import Annotated

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.module.infrastructure.container import Container
from src.routers.dependencies import get_container

logger = logging.getLogger(__name__)

_CHECK_TIMEOUT_SECONDS = 3


class Health:
    """
    Class proxy Health.
    """

    def __init__(self):
        self.router = APIRouter()
        self.set_customized_router()

    @staticmethod
    def get_router():
        health = Health()
        return health.router

    def set_customized_router(self):

        @self.router.get("/live")
        async def liveness():
            """
            The process is up. Used by container orchestrators to restart it.
            """
            return {"status": "ok"}

        @self.router.get("/ready")
        async def readiness(container: Annotated[Container, Depends(get_container)]):
            """
            The process can serve requests: database, storage and queue are reachable.
            """
            checks = {
                "database": container.user_repository.ping(),
                "storage": container.storage.ping(),
                "queue": container.queue.ping(),
            }
            results = {}
            for name, check in checks.items():
                try:
                    await asyncio.wait_for(check, _CHECK_TIMEOUT_SECONDS)
                    results[name] = "ok"
                except Exception as e:
                    logger.warning("Readiness check %s failed: %s", name, e)
                    results[name] = "unavailable"
            healthy = all(result == "ok" for result in results.values())
            return JSONResponse(
                status_code=200 if healthy else 503,
                content={
                    "status": "ok" if healthy else "unavailable",
                    "checks": results,
                },
            )
