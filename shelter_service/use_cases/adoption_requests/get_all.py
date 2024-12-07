from typing import Any
from domain.users import User, UserRole
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository


class GetAllRequestsUseCase:
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
            user_id: str,
            offset: int = 0,
            limit: int | None = None,
    ) -> list[Any]:
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        if not user and user.role not in self.available_roles:
            raise PermissionError('Get adoption requests is forbidden')
            
        adoption_requests: list[Any] = await self.adoption_requests_repo.get_all(
            offset=offset,
            limit=limit,
        )
        return adoption_requests
    