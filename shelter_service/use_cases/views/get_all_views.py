from typing import Any
from domain.users import User, UserRole

from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository


class GetAllAnimalViewsUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            views_repo: AnimalViewBaseRepository,
            available_roles: list[UserRole] = UserRole.ADMIN.value,
    ):
        self.user_repo = user_repo
        self.views_repo = views_repo
        self.available_roles = available_roles

    async def execute(
            self,
            user_id: str,
            offset: int = 0,
            limit: int | None = None,
    ) -> list[Any]:
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        if not user or user.role not in self.available_roles:
            raise PermissionError('Get all animal views is forbidden')

        return await self.views_repo.get_all(offset=offset, limit=limit)
