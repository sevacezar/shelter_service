from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from domain.animals import Image
from repositories.base.image_base_repo import BaseAnimalImageRepository

class AnimalImageMongoRepository(BaseAnimalImageRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection: AsyncIOMotorCollection = db['images']

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._collection

    def _get_image_obj_with_str_id(self, image_dict: dict) -> Image:
        if image_dict.get('_id'):
            image_dict['id'] = str(image_dict.pop('_id'))
        return Image(**image_dict)

    async def create(self, image: Image) -> Image:
        image_dict: dict = image.to_dict()
        del image_dict['id']
        res = await self._collection.insert_one(image_dict)
        image.id = str(res.inserted_id)
        return image

    async def get_by_id(self, id: str) -> Image | None:
        _id: ObjectId = ObjectId(id)
        res = await self._collection.find_one(filter={'_id': _id})
        if not res:
            return None
        return self._get_image_obj_with_str_id(image_dict=res)

    async def get_by_animal_id(self, animal_id: str) -> list[Any]:
        images = self._collection.find(filter={'animal_id': animal_id})
        return [self._get_image_obj_with_str_id(image_dict=i_image)
                async for i_image in images]

    async def delete(self, image: Image) -> None:
        _id: ObjectId = ObjectId(image.id)
        await self._collection.delete_one(filter={'_id': _id})

    async def set_avatar(self, image: Image) -> Image:
        _id: ObjectId = ObjectId(image.id)
        setting_avatar_res = await self._collection.update_one(
            filter={'_id': _id},
            update={'$set': {'is_avatar': True}},
        )
        image.is_avatar = True
        removing_avatar_res = await self._collection.update_many(
            filter={
                'animal_id': image.animal_id,
                '_id': {'$ne': _id},
            },
            update={'$set': {'is_avatar': False}},
        )
        return image

    async def update_description(self, image: Image, description: str) -> Image:
        _id: ObjectId = ObjectId(image.id)
        res = await self._collection.update_one(
            filter={'_id': _id},
            update={'$set': {'description': description}},
        )
        image.description = description
        return image
