from abc import ABC, abstractmethod
from typing import Any

from domain.adoption_requests import AdoptionRequest

class AdoptionRequestBaseRepository(ABC):
    @abstractmethod
    async def create(self, request: AdoptionRequest) -> AdoptionRequest:
        """Creates new adoption request"""
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> AdoptionRequest | None:
        """Gets adoption request by id or None"""
        pass

    @abstractmethod
    async def update_status(self, id: str, new_status: str) -> AdoptionRequest | None:
        """Updates adoption request by id with new status"""
        pass

    @abstractmethod
    async def delete_by_id(self, id: str) -> None:
        """Deletes adoption request by id"""
        pass
    
    @abstractmethod
    async def list_by_animal(self, animal_id: str) -> list[Any]:
        """Gets adoption requests list of specific animal"""
        pass

    @abstractmethod
    async def list_by_user(self, user_id: str) -> list[Any]:
        """Gets adoption requests list of specific user"""
        pass
