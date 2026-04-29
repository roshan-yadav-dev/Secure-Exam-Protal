from fastapi import FastAPI
from app.routes import health, version, dbtest

app = FastAPI()

app.include_router(health.router)
app.include_router(version.router, prefix="/api")
app.include_router(dbtest.router, prefix="/api")