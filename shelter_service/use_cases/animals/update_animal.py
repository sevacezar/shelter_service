from datetime import datetime
from typing import Any

from domain.animals import Animal, CoatType, AnimalGender, AnimalType, Status
from domain.users import UserRole, User
from repositories.base.animal_base_repo import AnimalBaseRepository
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import AnimalNotFound

class UpdateAnimalByIdUseCase:
    def __init__(
            self,
            animal_repo: AnimalBaseRepository,
            user_repo: UserBaseRepository,
            available_roles: list[UserRole] = UserRole.ADMIN.value,
        ):
        self.animal_repo = animal_repo
        self.user_repo = user_repo
        self.available_roles = available_roles

    async def execute(
            self,
            user_id: str,
            animal_id: str,
            updated_params: dict[str, Any],
    ) -> Animal:
        user: User = await self.user_repo.get_by_id(id=user_id)
        if not user or not user.role in self.available_roles:
            raise PermissionError('Create animal is forbidden')

        animal_to_update: Animal | None = await self.animal_repo.get_by_id(id=animal_id)
        if not animal_to_update:
            raise AnimalNotFound('Animal not found.')

        updated_animal: Animal = await self.animal_repo.update(
            animal=animal_to_update,
            updated_params=updated_params,
        )

        return updated_animal
