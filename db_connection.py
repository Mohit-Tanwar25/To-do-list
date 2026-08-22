import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI") or "mongodb://localhost:27017/"
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "todo_app")

client = None

def get_database():
    global client
    if client is None:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client[MONGO_DB_NAME]

def get_tasks_collection():
    db = get_database()
    return db["tasks"]
