from typing import Any
from domain.animals import Image
from repositories.base.image_base_repo import BaseAnimalImageRepository

class GetImagesByAnimalIdUseCase:
    def __init__(
            self,
            image_repo: BaseAnimalImageRepository,
    ):
        self.image_repo = image_repo

    async def execute(
            self,
            animal_id: str,
        ) -> list[Any]:

        images: list[Any] = await self.image_repo.get_by_animal_id(animal_id=animal_id)
        return images
    
