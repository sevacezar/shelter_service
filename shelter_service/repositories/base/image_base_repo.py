from abc import ABC, abstractmethod
from typing import Any

from domain.animals import Image


class BaseAnimalImageRepository:
    @abstractmethod
    async def create(self, image: Image) -> Image:
        """Creates new animal image"""
        pass

    @abstractmethod
    async def get_by_animal_id(self, animal_id: str) -> list[Any]:
        """Returns list of animal image by its id"""
        pass

    @abstractmethod
    async def delete(self, image_id: str) -> None:
        """Deletes animal image"""
        pass
