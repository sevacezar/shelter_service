from abc import ABC, abstractmethod


class BaseStorageService(ABC):
    @abstractmethod
    async def save(self, file_content: bytes, filename: str) -> str:
        """Saves file and return its path"""
        pass
