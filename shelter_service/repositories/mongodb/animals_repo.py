from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from domain.animals import Animal
from repositories.base.animal_base_repo import AnimalBaseRepository

class AnimalMongoRepository(AnimalBaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection: AsyncIOMotorCollection = db['animals']

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._collection
    
    async def create(self, animal):
        return await super().create(animal)
    
    async def get_by_id(self, id):
        return await super().get_by_id(id)
    
    async def update(self, animal, updated_params):
        return await super().update(animal, updated_params)
    
    async def get_all(self, offset = 0, limit = None):
        return await super().get_all(offset, limit)
    
    async def delete(self, animal):
        return await super().delete(animal)
    
    async def get_filtered(self, filters, offset = 0, limit = None):
        return await super().get_filtered(filters, offset, limit)