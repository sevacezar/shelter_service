from domain.animals import Image
from repositories.base.image_base_repo import BaseAnimalImageRepository
from repositories.base.image_base_storage import BaseStorageService

class AddImageUseCase:
    def __init__(
            self,
            image_repo: BaseAnimalImageRepository,
            storage_service: BaseStorageService,
    ):
        self.image_repo = image_repo
        self.storage_service = storage_service

    async def execute(
            self,
            animal_id: str,
            file_content: bytes,
            filename: str,
            description: str = None,
            is_avatar: bool = False,
        ) -> Image:

        filepath: str = await self.storage_service.save(
            file_content=file_content,
            filename=filename,
        )

        image: Image = Image(
            filename=filename,
            relative_path=filepath,
            description=description,
            is_avatar=is_avatar,
        )

        return await self.image_repo.create(image=image)
