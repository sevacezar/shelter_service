from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from domain.users import User, UserRole
from repositories.base.user_base_repo import UserBaseRepository

class UserMongoRepository(UserBaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection: AsyncIOMotorCollection = db['users']

    async def create(self, user) -> User:
        user_dict: dict = user.to_dict()
        if not user.get('id'):
            del user_dict['id']
        res = await self.collection.insert_one(user_dict)
        user.id = str(res.inserted_id)
        return user
    
    async def get_by_email(self, email) -> User | None:
        res = await self.collection.find_one(filter={'email': email})
        if res:
            return User(**res)
        return None
    
    