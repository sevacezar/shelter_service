from typing import Any
from domain.users import UserRole, User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserNotFound

class UpdateUserByIdUseCase:
    def __init__(self, user_repo: UserBaseRepository):
        self.user_repo = user_repo
    
    async def execute(
        self,
        cur_user_id: str,
        updated_user_id: str,
        updated_params: dict[str, Any],
    ) -> User | None:
        cur_user: User | None = await self.user_repo.get_by_id(id=cur_user_id)
        if not cur_user:
            raise UserNotFound('User with passed id not found')
        
        if not (cur_user.id == updated_user_id or cur_user.role == UserRole.ADMIN.value):
            raise PermissionError('User information can update only admin or same user.')
        
        updated_user: User = await self.user_repo.update_by_id(
            id=updated_user_id,
            updated_params=updated_params,
        )
        return updated_user
