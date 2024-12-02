from typing import Any
from domain.users import UserRole, User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserNotFound

class UpdateUserByIdUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            available_roles: list[UserRole] = [UserRole.ADMIN.value],
        ):
        self.user_repo = user_repo
        self.available_roles = available_roles

    async def execute(
        self,
        cur_user_id: str,
        updated_user_id: str,
        updated_params: dict[str, Any],
    ) -> User | None:
        cur_user: User | None = await self.user_repo.get_by_id(id=cur_user_id)
        if not cur_user:
            raise UserNotFound('User with passed id not found')

        if not (cur_user.id == updated_user_id or cur_user.role in self.available_roles):
            raise PermissionError('User information can update only admin or same user.')

        user_to_update: User | None = await self.user_repo.get_by_id(id=updated_user_id)
        if not user_to_update:
            raise UserNotFound(f'Updated user not found')

        updated_user: User = await self.user_repo.update(
            user=user_to_update,
            updated_params=updated_params,
        )
        return updated_user
