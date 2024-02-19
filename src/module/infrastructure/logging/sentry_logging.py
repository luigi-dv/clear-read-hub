from fastapi import FastAPI

from sentry_sdk.integrations.asgi import SentryAsgiMiddleware


class SentryLogger:
    def __init__(self, app: FastAPI):
        self.app = app

    def add_sentry_middleware(self):
        try:
            self.app.add_middleware(SentryAsgiMiddleware)
        except Exception as e:
            pass  # Do nothing
