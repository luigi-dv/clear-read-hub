"""
    Global Modules
"""
import sentry_sdk
import uvicorn
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

"""
    API Modules
"""
from src.routers.routes import router
from src.core.globals import get_application

# Add explicit app name
app = get_application()

# Add the routes to the app
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', reload=True)