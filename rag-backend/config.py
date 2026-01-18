import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")

DB_NAME = "myProject"
COLLECTION_NAME = "rag_app"
VECTOR_INDEX_NAME = "vector_index"
CLERK_JWT_PUBLIC_KEY = os.getenv("CLERK_JWT_PUBLIC_KEY")
if not CLERK_JWT_PUBLIC_KEY:
    raise ValueError("CLERK_JWT_PUBLIC_KEY missing from .env")