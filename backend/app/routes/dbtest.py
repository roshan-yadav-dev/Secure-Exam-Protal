from fastapi import APIRouter
from app.database import users

router = APIRouter()

@router.post("/insert-user")
def insert_user():
    data = {
        "name": "Roshan",
        "email": "roshan@test.com",
        "role": "student"
    }

    result = users.insert_one(data)

    return {
        "message": "Inserted",
        "id": str(result.inserted_id)
    }