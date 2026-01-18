from datetime import datetime
from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db["chat_history"]


def save_message(
    session_id: str,
    user_id: str,
    role: str,
    content: str
):
    collection.insert_one({
        "session_id": session_id,
        "user_id": user_id,          
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })


def get_recent_messages(
    session_id: str,
    user_id: str,
    limit: int = 5
):
    messages = collection.find(
        {
            "session_id": session_id,
            "user_id": user_id        
        }
    ).sort("timestamp", -1).limit(limit)

    return list(reversed([
        m["content"]
        for m in messages
        if m["role"] == "user"
    ]))
