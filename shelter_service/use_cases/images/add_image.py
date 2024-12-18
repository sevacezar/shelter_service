from domain.animals import Image
from domain.users import UserRole, User
from repositories.base.image_base_repo import BaseAnimalImageRepository
from repositories.base.image_base_storage import BaseStorageService
from repositories.base.user_base_repo import UserBaseRepository

class AddImageUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            image_repo: BaseAnimalImageRepository,
            storage_service: BaseStorageService,
            available_roles: list[UserRole],
    ):
        self.user_repo = user_repo
        self.image_repo = image_repo
        self.storage_service = storage_service
        self.available_roles = available_roles

    async def execute(
            self,
            user_id: str,
            animal_id: str,
            file_content: bytes,
            filename: str,
            description: str = None,
            is_avatar: bool = False,
        ) -> Image:
        user: User = await self.user_repo.get_by_id(id=user_id)
        if not user or not user.role in self.available_roles:
            raise PermissionError('Create animal is forbidden')

        filepath: str = await self.storage_service.save(
            file_content=file_content,
            filename=filename,
            animal_id=animal_id,
        )

        image: Image = Image(
            animal_id=animal_id,
            filename=filename,
            relative_path=filepath,
            description=description,
            is_avatar=is_avatar,
        )

        return await self.image_repo.create(image=image)
