from domain.animal_views import AnimalView
from domain.users import User, UserRole

from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository

from use_cases.exceptions import AnimalViewNotFound

class DeleteAnimalViewUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            views_repo: AnimalViewBaseRepository,
            available_roles: list[UserRole] = UserRole.ADMIN.value,
    ):
        self.user_repo = user_repo
        self.views_repo = views_repo
        self.available_roles = available_roles

    async def execute(
            self,
            user_id: str,
            view_id: str,
    ) -> None:
        user: User | None = await self.user_repo.get_by_id(id=user_id)
        if (not user) or (user.role not in self.available_roles):
            raise PermissionError('Delete animal view is forbidden')
        
        animal_view: AnimalView | None = await self.views_repo.get_by_id(id=view_id)
        if not animal_view:
            raise AnimalViewNotFound('Animal view not found')

        return await self.views_repo.delete(view=animal_view)
    