from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from domain.animal_views import AnimalView
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository

class AnimalViewMongoRepository(AnimalViewBaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection: AsyncIOMotorCollection = db['animal_views']

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._collection

    def _get_view_obj_with_str_ids(self, view_dict: dict) -> AnimalView:
        if view_dict.get('_id'):
            view_dict['id'] = str(view_dict.pop('_id'))
        view_dict['animal_id'] = str(view_dict['animal_id'])
        view_dict['user_id'] = str(view_dict['user_id'])
        return AnimalView(**view_dict)

    async def create(self, view: AnimalView) -> AnimalView:
        animal_view_dict: dict = view.to_dict()
        del animal_view_dict['id']
        animal_view_dict['user_id'] = ObjectId(animal_view_dict.get('user_id'))
        animal_view_dict['animal_id'] = ObjectId(animal_view_dict.get('animal_id'))
        res = await self._collection.insert_one(animal_view_dict)
        view.id = str(res.inserted_id)
        return view

    async def get_by_id(self, id: str) -> AnimalView | None:
        _id: ObjectId = ObjectId(id)
        res = await self._collection.find_one({'_id': _id})
        if not res:
            return None
        return self._get_view_obj_with_str_ids(view_dict=res)

    async def delete(self, view: AnimalView) -> None:
        _id: ObjectId = ObjectId(view.id)
        await self._collection.delete_one({'_id': _id})

    async def list_by_animal(self, animal_id: str) -> list[Any]:
        _animal_id: ObjectId = ObjectId(animal_id)
        cursor = self._collection.find({'animal_id': _animal_id})
        views: list[AnimalView] = []
        async for doc in cursor:
            views.append(self._get_view_obj_with_str_ids(view_dict=doc))
        return views

    async def list_by_user(self, user_id: str) -> list[Any]:
        _user_id: ObjectId = ObjectId(user_id)
        cursor = self._collection.find({'user_id': _user_id})
        views: list[AnimalView] = []
        async for doc in cursor:
            views.append(self._get_view_obj_with_str_ids(view_dict=doc))
        return views

    async def get_all(self, offset: int = 0, limit: int | None = None) -> list[Any]:
        cursor = self._collection.find({})
        if offset > 0:
            cursor = cursor.skip(offset)
        if limit:
            cursor = cursor.limit(limit)
        views: list[AnimalView] = []
        async for doc in cursor:
            views.append(self._get_view_obj_with_str_ids(view_dict=doc))
        return views

