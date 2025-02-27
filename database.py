from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

db_client = AsyncIOMotorClient(MONGO_URI)
db = db_client["telegram_file_bot"]
collection = db["files"]
