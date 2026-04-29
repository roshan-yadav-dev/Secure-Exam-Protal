from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.version import router as version_router
from app.config import APP_NAME

app = FastAPI(title=APP_NAME)

app.include_router(health_router)
app.include_router(version_router)
print(APP_NAME)