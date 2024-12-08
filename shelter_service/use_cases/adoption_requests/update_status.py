from domain.adoption_requests import AdoptionRequest, RequestStatus
from domain.users import User, UserRole
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository
from use_cases.exceptions import AdoptionRequestNotFound


class UpdateStatusRequestUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            adoption_requests_repo: AdoptionRequestBaseRepository,
            available_roles: list[UserRole] = [UserRole.ADMIN.value],
            available_statuses_for_users: list[str] = [RequestStatus.CANCELLED.value]
    ):
        self.user_repo = user_repo
        self.adoption_requests_repo = adoption_requests_repo
        self.available_roles = available_roles
        self.available_statuses_for_users = available_statuses_for_users

    async def execute(
            self,
            user_id: str,
            request_id: str,
            new_status: str,

    ) -> AdoptionRequest:
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        if not user:
            raise PermissionError('Update adoption requests status is forbidden for anonym users')
        
        if (user.role not in self.available_roles) and (new_status not in self.available_statuses_for_users):
            raise PermissionError(f'User can not update status on {new_status}')
    
        adoption_request: AdoptionRequest | None = await self.adoption_requests_repo.get_by_id(id=request_id)
        if not adoption_request:
            raise AdoptionRequestNotFound('Adoption request is not found')
        
        if (user.role not in self.available_roles) and (adoption_request.user_id != user.id):
            raise PermissionError('User can not update foreign adoption request')
        
        return await self.adoption_requests_repo.update_status(request=adoption_request, new_status=new_status)
