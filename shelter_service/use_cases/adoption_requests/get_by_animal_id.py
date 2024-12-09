from typing import Any
from domain.users import User, UserRole
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository


class GetRequestsByAnimalIdUseCase:
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
            animal_id: str,
    ) -> list[Any]:
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        if not (user and user.role in self.available_roles):
            raise PermissionError('Get adoption requests by animal_id is forbidden')
            
        adoption_requests: list[Any] = await self.adoption_requests_repo.list_by_animal(animal_id=animal_id)
        return adoption_requests