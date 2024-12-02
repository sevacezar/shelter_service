from domain.users import UserRole, User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserNotFound

class GetUserByIdUseCase:
    def __init__(self, user_repo: UserBaseRepository):
        self.user_repo = user_repo
    
    async def execute(
        self,
        cur_user_id: str,
        searched_user_id: str,
    ) -> User | None:
        cur_user: User | None = await self.user_repo.get_by_id(id=cur_user_id)
        if not cur_user:
            raise UserNotFound('User with passed id not found')
        
        if not (cur_user.id == searched_user_id or cur_user.role == UserRole.ADMIN.value):
            raise PermissionError('User information can get only admin or same user.')
        
        searched_user: User = await self.user_repo.get_by_id(id=searched_user_id)
        return searched_user
