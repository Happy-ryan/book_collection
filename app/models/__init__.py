from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import MONGO_DB_NAME, MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
engine = AIOEngine(client=client, database=MONGO_DB_NAME)

class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None
    
    
    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.engine = AIOEngine(client=client, database=MONGO_DB_NAME)
        print("db와 성공적으로 연결되었습니다.")


    def close(self):
        self.client.close()
mongodb = MongoDB()