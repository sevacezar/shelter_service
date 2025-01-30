from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection


class MongoDBManager:
    def __init__(
            self,
            host: str = 'localhost',
            port: str | int = 27017,
            username: str | None = None,
            password: str | None = None,
            db_name: str = 'SHELTER',
        ) -> None:
        port = str(port)
        if username and password:
            self._db_url = f'mongodb://{username}:{password}@{host}:{port}'
        else:
            self._db_url = f'mongodb://{host}:{port}'
        self._client: AsyncIOMotorClient = AsyncIOMotorClient(self._db_url)
        self._db: AsyncIOMotorDatabase = self._client[db_name]
    
    def get_collection(self, name: str) -> AsyncIOMotorCollection:
        return self._db[name]
    
    def get_db(self):
        return self._db
    

    