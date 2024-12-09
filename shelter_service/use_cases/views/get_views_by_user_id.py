from typing import Any
from domain.users import User, UserRole

from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository


class GetViewsByUserIdUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            views_repo: AnimalViewBaseRepository,
            available_roles: list[UserRole] = [UserRole.ADMIN.value],
    ):
        self.user_repo = user_repo
        self.views_repo = views_repo
        self.available_roles = available_roles

    async def execute(
            self,
            cur_user_id: str,
            target_user_id: str,
    ) -> list[Any]:
        user: User | None = await self.user_repo.get_by_id(id=cur_user_id)
        if not user:
            raise PermissionError('Get all animal views is forbidden')
        if (user.role not in self.available_roles) and (cur_user_id != target_user_id):
            raise PermissionError('Get all animal views of foreign user is forbidden for current user')

        return await self.views_repo.list_by_user(user_id=target_user_id)
