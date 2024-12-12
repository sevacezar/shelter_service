from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from domain.users import User, UserRole
from repositories.base.user_base_repo import UserBaseRepository

class UserMongoRepository(UserBaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection: AsyncIOMotorCollection = db['users']

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._collection
    
    def _get_user_obj_with_str_id(user_dict: dict) -> User:
        if user_dict.get('_id'):
            user_dict['id'] = str(user_dict.pop('_id'))
        return User(**user_dict)

    async def create(self, user: User) -> User:
        user_dict: dict = user.to_dict()
        del user_dict['id']
        res = await self._collection.insert_one(user_dict)
        user.id = str(res.inserted_id)
        return user

    async def get_by_email(self, email: str) -> User | None:
        res = await self._collection.find_one(filter={'email': email})
        if res:
            return User(self._get_user_obj_with_str_id(user_dict=res))
        return None

    async def get_by_id(self, id: str) -> User | None:
        _id: ObjectId = ObjectId(id)
        res = await self._collection.find_one(filter={'_id': _id})
        if not res:
            return None
        return self._get_user_obj_with_str_id(user_dict=res)

    async def update(self, user: User, updated_params: dict[str, Any]) -> User:
        _id: ObjectId = ObjectId(user.id)
        updated_user: User = user.update(params=updated_params)
        updated_user_dict: dict = updated_user.to_dict()
        del updated_user_dict['id']
        res = await self._collection.replace_one(filter={'_id': _id}, replacement=updated_user_dict)
        return updated_user

    async def delete(self, user: User) -> None:
        _id: ObjectId = ObjectId(user.id)
        await self._collection.delete_one(filter={'_id': _id})

    async def get_all(self, offset: int = 0, limit: int | None = None) -> list[Any]:
        users: list[User] = []
        cursor = self._collection.find()
        if offset > 0:
            cursor = cursor.skip(offset)
        if limit:
            cursor = cursor.limit(limit)
        async for doc in cursor:
            users.append(self._get_user_obj_with_str_id(user_dict=doc))
        return users
