from domain.animals import Animal
from domain.adoption_requests import AdoptionRequest, RequestStatus
from domain.users import User

from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_base_repo import AnimalBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository

from use_cases.exceptions import AnimalNotFound

class CreateRequestUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            animal_repo: AnimalBaseRepository,
            adoption_requests_repo: AdoptionRequestBaseRepository,
    ):
        self.user_repo = user_repo
        self.animal_repo = animal_repo
        self.adoption_requests_repo = adoption_requests_repo

    async def execute(
            self,
            user_id: str,
            animal_id: str,
            comment: str,
    ) -> AdoptionRequest:
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        if not user:
            raise PermissionError('Create adoption requests is forbidden for anonym users')
        
        animal: Animal | None = await self.animal_repo.get_by_id(id=animal_id)
        if not animal:
            raise AnimalNotFound('Animal not found')
        
        adoption_request: AdoptionRequest = AdoptionRequest(
            user_id=user_id,
            animal_id=animal_id,
            status=RequestStatus.PENDING.value,
            user_comment=comment,
        )
        return await self.adoption_requests_repo.create(request=adoption_request)
    