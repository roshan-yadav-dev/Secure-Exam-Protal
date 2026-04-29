from pymongo import MongoClient
from app.config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users = db["users"]
exams = db["exams"]
questions = db["questions"]
submissions = db["submissions"]
logs = db["logs"]