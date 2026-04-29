from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URI)

db = client[settings.DB_NAME]

# Collections
users = db["users"]
exams = db["exams"]
questions = db["questions"]
submissions = db["submissions"]
logs = db["logs"]