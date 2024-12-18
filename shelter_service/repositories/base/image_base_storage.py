from abc import ABC, abstractmethod


class BaseStorageService(ABC):
    @abstractmethod
    async def save(self, file_content: bytes, filename: str, animal_id: str) -> str:
        """Saves file and return its path"""
        pass

    @abstractmethod
    async def delete(self, relative_file_path: str) -> bool:
        """Deletes file by filepath"""
        pass