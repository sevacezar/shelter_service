from domain.animals import Image
from domain.users import UserRole, User
from repositories.base.image_base_repo import BaseAnimalImageRepository
from repositories.base.image_base_storage import BaseStorageService
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import ImageNotFound

class DeleteImageUseCase:
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
            image_id: str,
        ) -> None:
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        if not user or not user.role in self.available_roles:
            raise PermissionError('Create animal is forbidden')

        image: Image | None = await self.image_repo.get_by_id(id=image_id)
        if not image:
            raise ImageNotFound('Image not found')

        await self.storage_service.delete(file_path=image.relative_path)

        await self.image_repo.delete(image=image)
