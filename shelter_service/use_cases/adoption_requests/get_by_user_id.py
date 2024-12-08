from typing import Any
from domain.users import User, UserRole
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository


class GetRequestsByUserIdUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            adoption_requests_repo: AdoptionRequestBaseRepository,
            available_roles: list[UserRole] = [UserRole.ADMIN.value],
    ):
        self.user_repo = user_repo
        self.adoption_requests_repo = adoption_requests_repo
        self.available_roles = available_roles

    async def execute(
            self,
            cur_user_id: str,
            user_id_to_search: str,
    ) -> list[Any]:
        cur_user: User | None = await self.user_repo.get_by_id(id=cur_user_id)
        if not cur_user:
            raise PermissionError('Get adoption requests is forbidden for anonym users')
        if (cur_user.id != user_id_to_search) and (cur_user.role not in self.available_roles):
            raise PermissionError('Get adoption requests of this user is forbidden for current user')
        adoption_requests: list[Any] = await self.adoption_requests_repo.list_by_user(user_id=user_id_to_search)
        return adoption_requests
