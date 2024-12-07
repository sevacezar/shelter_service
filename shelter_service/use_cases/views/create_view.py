from domain.animals import Animal
from domain.animal_views import AnimalView
from domain.users import User

from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_base_repo import AnimalBaseRepository
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository

from use_cases.exceptions import AnimalNotFound

class CreateAnimalViewUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            animal_repo: AnimalBaseRepository,
            views_repo: AnimalViewBaseRepository,
    ):
        self.user_repo = user_repo
        self.animal_repo = animal_repo
        self.views_repo = views_repo

    async def execute(
            self,
            animal_id: str,
            user_id: str | None = None,
    ) -> AnimalView:
        animal: Animal | None = await self.animal_repo.get_by_id(id=animal_id)
        if not animal:
            raise AnimalNotFound('Animal not found')
        
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        user_id: str | None = user.id if user else None
        animal_view: AnimalView = AnimalView(
            animal_id=animal_id,
            user_id=user_id,
        )
        return await self.views_repo.create(view=animal_view)
    