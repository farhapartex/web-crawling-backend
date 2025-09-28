from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    _instance = None
    _client = None
    _database = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def connect(self) -> Database:
        if self._client is None:
            mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            db_name = os.getenv("MONGODB_DB_NAME", "book_scraping")

            self._client = MongoClient(mongodb_url)
            self._database = self._client[db_name]
        return self._database

    def get_collection(self, collection_name: str) -> Collection:
        if self._database is None:
            self.connect()
        return self._database[collection_name]

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._database = None

db_connection = DatabaseConnection()