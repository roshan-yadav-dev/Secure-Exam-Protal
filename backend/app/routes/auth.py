from fastapi import APIRouter, HTTPException
from app.database import db
from app.utils.hash import hash_password, verify_password
from app.utils.token import create_access_token
from app.models.user import user_schema
from fastapi import Depends
from app.middleware.auth import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])

users = db["users"]

@router.post("/register")
def register(data: dict):

    if users.find_one({"email": data["email"]}):
        raise HTTPException(400, "Email already exists")

    new_user = {
        "name": data["name"],
        "email": data["email"],
        "password": hash_password(data["password"]),
        "role": data["role"]   # student/examiner
    }

    users.insert_one(new_user)

    return {"message": "User Registered"}

#----Login Endpoint----#
@router.post("/login")
def login(data: dict):

    user = users.find_one({"email": data["email"]})

    if not user:
        raise HTTPException(401, "Invalid credentials")

    if not verify_password(data["password"], user["password"]):
        raise HTTPException(401, "Wrong password")

    token = create_access_token({
        "id": str(user["_id"]),
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(user = Depends(get_current_user)):
    return user