from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "health_db")


_client: Optional[AsyncIOMotorClient] = None
db = None


async def connect_to_mongo() -> None:
    global _client, db
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URI)
        db = _client[DB_NAME]


async def close_mongo_connection() -> None:
    global _client, db
    if _client:
        _client.close()
    _client = None
    db = None


def get_collection(name: str):
    if db is None:
        raise RuntimeError("Database not connected yet!")
    return db[name]
