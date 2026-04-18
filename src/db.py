import os
from contextlib import contextmanager
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://admin:test@localhost:27017/?authSource=admin&readPreference=primary&ssl=false"
)

@contextmanager
def get_mongo_client():
    """
    Context manager for creating and automatically closing
    a MongoDB client connection.

    Yields:
        MongoClient: An active connection to the MongoDB server.
    """
    client = MongoClient(MONGO_URI)
    try:
        yield client
    finally:
        client.close()
