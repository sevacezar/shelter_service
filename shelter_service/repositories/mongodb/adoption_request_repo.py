from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from domain.adoption_requests import AdoptionRequest
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository

class AdoptionRequestMongoRepository(AdoptionRequestBaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection: AsyncIOMotorCollection = db['adoption_requests']

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._collection

    def _get_view_obj_with_str_ids(self, request_dict: dict) -> AdoptionRequest:
        if request_dict.get('_id'):
            request_dict['id'] = str(request_dict.pop('_id'))
        request_dict['animal_id'] = str(request_dict['animal_id'])
        request_dict['user_id'] = str(request_dict['user_id'])
        return AdoptionRequest(**request_dict)

    async def create(self, request: AdoptionRequest) -> AdoptionRequest:
        adoption_request_dict: dict = request.to_dict()
        del adoption_request_dict['id']
        adoption_request_dict['user_id'] = ObjectId(adoption_request_dict.get('user_id'))
        adoption_request_dict['animal_id'] = ObjectId(adoption_request_dict.get('animal_id'))
        res = await self._collection.insert_one(adoption_request_dict)
        request.id = str(res.inserted_id)
        return request

    async def get_by_id(self, id: str) -> AdoptionRequest | None:
        _id: ObjectId = ObjectId(id)
        res = await self._collection.find_one({'_id': _id})
        if not res:
            return None
        return self._get_view_obj_with_str_ids(view_dict=res)

    async def update_status(self, request: AdoptionRequest, new_status: str) -> AdoptionRequest:
        _id: ObjectId = ObjectId(request.id)
        updated_request: AdoptionRequest = request.update(params={'status': new_status})
        res = await self._collection.update_one(filter={'_id': _id}, update={'$set': {'status': new_status}})
        return updated_request

    async def delete(self, request: AdoptionRequest) -> None:
        _id: ObjectId = ObjectId(request.id)
        await self._collection.delete_one({'_id': _id})

    async def list_by_animal(self, animal_id: str) -> list[Any]:
        _animal_id: ObjectId = ObjectId(animal_id)
        cursor = self._collection.find({'animal_id': _animal_id})
        requests: list[AdoptionRequest] = []
        async for doc in cursor:
            requests.append(self._get_view_obj_with_str_ids(view_dict=doc))
        return requests

    async def list_by_user(self, user_id: str) -> list[Any]:
        _user_id: ObjectId = ObjectId(user_id)
        cursor = self._collection.find({'user_id': _user_id})
        requests: list[AdoptionRequest] = []
        async for doc in cursor:
            requests.append(self._get_view_obj_with_str_ids(view_dict=doc))
        return requests

    async def get_all(self, offset: int = 0, limit: int | None = None) -> list[Any]:
        cursor = self._collection.find({})
        if offset > 0:
            cursor = cursor.skip(offset)
        if limit:
            cursor = cursor.limit(limit)
        requests: list[AdoptionRequest] = []
        async for doc in cursor:
            requests.append(self._get_view_obj_with_str_ids(view_dict=doc))
        return requests
