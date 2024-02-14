from fastapi import FastAPI, Request, HTTPException

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration


class SentryLogger:
    def __init__(self, app: FastAPI):
        self.app = app

    def add_sentry_middleware(self):
        try:
            self.app.add_middleware(SentryAsgiMiddleware)
        except Exception as e:
            pass  # Do nothing