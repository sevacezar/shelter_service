from abc import ABC, abstractmethod
from typing import Any

from domain.animals import Animal, Image

class AnimalBaseRepository(ABC):
    @abstractmethod
    async def create(self, animal: Animal) -> Animal:
        """Creates new animal"""
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Animal | None:
        """Gets animal by id or None"""
        pass

    @abstractmethod
    async def update(self, animal: Animal, updated_params: dict[str, Any]) -> Animal | None:
        """Updates animal using passed params for update"""
        pass

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int | None = None) -> list[Any]:
        """Gets all animals with offset and limit"""
        pass

    @abstractmethod
    async def delete(self, animal: Animal) -> None:
        """Deletes animal"""
        pass

    @abstractmethod
    async def get_filtered(
        self,
        filters: dict[str, list],
        offset: int = 0,
        limit: int | None = None,
    ) -> list[Any]:
        """Gets animals with passed filters"""
        pass


class ImageBaseRepository(ABC):
    @abstractmethod
    async def create(self, image: Image) -> Image:
        """Creates animal image"""
        pass

    @abstractmethod
    async def get_by_animal_id(self, animal_id: str) -> list[Any]:
        """Gets list of animal images for specific animal by id"""
        pass

    @abstractmethod
    async def delete_by_id(self, id: str) -> None:
        """Deletes animal image by id"""
        pass
