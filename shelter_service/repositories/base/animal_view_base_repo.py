from abc import ABC, abstractmethod
from typing import Any

from domain.animal_views import AnimalView

class AnimalViewBaseRepository(ABC):
    @abstractmethod
    async def create(self, view: AnimalView) -> AnimalView:
        """Creates new animal view"""
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> AnimalView | None:
        """Gets animal view by id or None"""
        pass

    @abstractmethod
    async def delete_by_id(self, id: str) -> None:
        """Deletes animal view by id"""
        pass
    
    @abstractmethod
    async def list_by_animal(self, animal_id: str) -> list[Any]:
        """Gets animal view list of specific animal"""
        pass

    @abstractmethod
    async def list_by_user(self, user_id: str) -> list[Any]:
        """Gets animal view list of specific user"""
        pass
