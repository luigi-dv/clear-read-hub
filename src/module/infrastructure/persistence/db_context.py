from pymongo import MongoClient

# Import the service files file
from src.service_config import serviceConfig


class DatabaseContext:
    def __init__(self):
        self.client = MongoClient(serviceConfig.MONGO_INITDB_CONNECTION_STRING)
        self.database = self.client[serviceConfig.MONGODB_DATABASE_NAME]

    def get_client(self):
        return self.client

    def get_database(self):
        return self.database


if __name__ == "__main__":
    db_client = DatabaseContext()
    main_database = db_client.get_database()
