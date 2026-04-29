from fastapi import APIRouter
from app.config import APP_VERSION, APP_NAME

router = APIRouter()

@router.get("/version")
def version():
    return {
        "app": APP_NAME,
        "version": APP_VERSION
    }