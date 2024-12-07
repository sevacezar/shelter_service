from typing import Any
from domain.users import User, UserRole
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository


class GetRequestsByUserIdUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            adoption_requests_repo: AdoptionRequestBaseRepository,
    ):
        self.user_repo = user_repo
        self.adoption_requests_repo = adoption_requests_repo

    async def execute(
            self,
            user_id: str,
    ) -> list[Any]:
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        if not user:
            raise PermissionError('Get adoption requests is forbidden for anonym users')
            
        adoption_requests: list[Any] = await self.adoption_requests_repo.list_by_user(user_id=user_id)
        return adoption_requests
