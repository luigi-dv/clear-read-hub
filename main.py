"""
    Global Modules
"""
import uvicorn

"""
    API Modules
"""
from src.routers.routes import router
from src.core.globals import app

# Add explicit app name
app = app

# Add the routes to the app
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', reload=True)