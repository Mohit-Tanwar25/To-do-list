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
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=15000, connectTimeoutMS=15000, retryWrites=True)
    return client[MONGO_DB_NAME]

def get_tasks_collection():
    db = get_database()
    return db["tasks"]

def get_users_collection():
    db = get_database()
    return db["users"]

def init_db_indexes():
    """Initializes indexes for fast querying and isolation."""
    try:
        tasks = get_tasks_collection()
        tasks.create_index([("user_id", 1), ("date", 1)])
        tasks.create_index([("user_id", 1), ("status", 1)])
        
        users = get_users_collection()
        users.create_index("google_id", unique=True, sparse=True)
        users.create_index("email", unique=True, sparse=True)
    except Exception as e:
        print(f"Index initialization notice: {e}")
