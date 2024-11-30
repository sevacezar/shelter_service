from abc import ABC, abstractmethod
from typing import Any

from domain.users import User

class UserBaseRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        """Creates new user"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Gets user by email or None"""
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> User | None:
        """Gets user by id or None"""
        pass

    @abstractmethod
    async def update_by_id(self, id: str, updated_params: dict[str, Any]) -> User | None:
        """Updates user by id using passed params for update"""
        pass

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int | None = None) -> list[Any]:
        """Gets all users with offset and limit"""
        pass

    @abstractmethod
    async def delete_by_email(self, email: str) -> None:
        """Deletes user by email"""
        pass
    