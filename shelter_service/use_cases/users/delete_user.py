from domain.users import UserRole, User
from repositories.base.user_base_repo import UserBaseRepository


class DeleteUserUseCase:
    def __init__(self, user_repo: UserBaseRepository):
        self.user_repo = user_repo
    
    async def execute(
        self,
        admin_id: str,
        deleted_user_email: str,
    ):
        user: User | None = await self.user_repo.get_by_id(id=admin_id)
        if not user or user.role != UserRole.ADMIN.value:
            raise PermissionError('Only admin can delete user.')
 
        await self.user_repo.delete_by_email(email=deleted_user_email)
