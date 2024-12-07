from domain.adoption_requests import AdoptionRequest
from domain.users import User, UserRole
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository
from use_cases.exceptions import AdoptionRequestNotFound


class DeleteRequestUseCase:
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
            request_id: str,
    ) -> None:
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        if not user and user.role not in self.available_roles:
            raise PermissionError('Update adoption requests status is forbidden')
            
        adoption_request: AdoptionRequest | None = await self.adoption_requests_repo.get_by_id(id=request_id)
        if not adoption_request:
            raise AdoptionRequestNotFound('Adoption request is not found')
        
        return await self.adoption_requests_repo.delete(request=adoption_request)
