#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

import uvicorn
from src.routers.routes import router
from src.module.infrastructure.fastapi_init import get_application

# Start the FastAPI custom application
app = get_application()  # Path: src/module/infrastructure/fastapi_init.py

# Include the router
app.include_router(router)  # Path: src/routers/routes.py

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
