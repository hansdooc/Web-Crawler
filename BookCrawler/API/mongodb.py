# mongodb.py
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
#change MONGO_DATABASE to TEST_DATABASE for test crawling

mongo_uri = os.getenv('MONGO_URI')
mongo_db = os.getenv('MONGO_DATABASE')

async def connect_to_mongo():
    global client, database
    client = AsyncIOMotorClient(mongo_uri)
    database = client[mongo_db]
    return database

async def close_mongo_connection():
    global client
    if client:
        client.close()
