from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from domain.animals import Animal
from repositories.base.animal_base_repo import AnimalBaseRepository

class AnimalMongoRepository(AnimalBaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection: AsyncIOMotorCollection = db['animals']

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._collection

    def _get_animal_obj_with_str_id(self, animal_dict: dict) -> Animal:
        if animal_dict.get('_id'):
            animal_dict['id'] = str(animal_dict.pop('_id'))
        return Animal(**animal_dict)

    async def create(self, animal: Animal) -> Animal:
        animal_dict: dict = animal.to_dict()
        del animal_dict['id']
        res = await self._collection.insert_one(animal_dict)
        animal.id = str(res.inserted_id)
        return animal

    async def get_by_id(self, id: str) -> Animal | None:
        _id: ObjectId = ObjectId(id)
        res = await self._collection.find_one(filter={'_id': _id})
        if not res:
            return None
        return self._get_animal_obj_with_str_id(animal_dict=res)

    async def update(self, animal: Animal, updated_params: dict[str, Any]) -> Animal:
        _id: ObjectId = ObjectId(animal.id)
        updated_animal: Animal = animal.update(params=updated_params)
        updated_animal_dict: dict = updated_animal.to_dict()
        del updated_animal_dict['id']
        res = await self._collection.replace_one(filter={'_id': _id}, replacement=updated_animal_dict)
        return updated_animal

    async def get_all(self, offset = 0, limit = None) -> list[Any]:
        animals: list[Animal] = []
        cursor = self._collection.find()
        if offset > 0:
            cursor = cursor.skip(offset)
        if limit:
            cursor = cursor.limit(limit)
        async for doc in cursor:
            animals.append(self._get_animal_obj_with_str_id(animal_dict=doc))
        return animals

    async def delete(self, animal: Animal) -> None:
        _id: ObjectId = ObjectId(animal.id)
        await self._collection.delete_one(filter={'_id': _id})

    async def get_filtered(self, filters: dict[str, Any], offset = 0, limit = None):
        animals: list[Animal] = []
        filter_dict: dict = {key: {'$in': values} for key, values in filters.items()}
        cursor = self._collection.find(filter=filter_dict)
        if offset > 0:
            cursor = cursor.skip(offset)
        if limit:
            cursor = cursor.limit(limit)
        async for doc in cursor:
            animals.append(self._get_animal_obj_with_str_id(animal_dict=doc))
        return animals

    