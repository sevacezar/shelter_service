from domain.users import UserRole, User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserNotFound


class DeleteUserUseCase:
    def __init__(
            self,
            user_repo: UserBaseRepository,
            available_roles: list[UserRole] = [UserRole.ADMIN.value],
        ):
        self.user_repo = user_repo
        self.available_roles = available_roles

    async def execute(
        self,
        admin_id: str,
        deleted_user_email: str,
    ):
        user: User | None = await self.user_repo.get_by_id(id=admin_id)
        if not user or user.role not in self.available_roles:
            raise PermissionError('Delete user is forbidden.')

        deleted_user: User | None = await self.user_repo.get_by_email(email=deleted_user_email)
        if not deleted_user:
            raise UserNotFound(f'User with email {deleted_user_email} not found')

        await self.user_repo.delete(user=deleted_user)
