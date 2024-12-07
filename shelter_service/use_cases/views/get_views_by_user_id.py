from typing import Any
from domain.users import User, UserRole

from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository


class GetViewsByUserIdUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            views_repo: AnimalViewBaseRepository,
    ):
        self.user_repo = user_repo
        self.views_repo = views_repo

    async def execute(
            self,
            user_id: str,
    ) -> list[Any]:
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        if not user:
            raise PermissionError('Get all animal views is forbidden')

        return await self.views_repo.list_by_user(user_id=user_id)
