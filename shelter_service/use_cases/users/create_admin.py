from domain.users import UserRole, User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserAlreadyExists

class CreateAdminUseCase:
    def __init__(self, user_repo: UserBaseRepository):
        self.user_repo = user_repo

    async def execute(
        self,
        first_name: str,
        second_name: str,
        email: str,
        phone: str,
        password: str,
    ) -> User | None:
        admins: list[User] = await self.user_repo.get_admins()
        if not admins:
            hashed_password: str = User.get_password_hash(password=password)
            user = User(
                first_name=first_name,
                second_name=second_name,
                email=email,
                phone=phone,
                hashed_password=hashed_password,
                role=UserRole.ADMIN.value,
            )
            return await self.user_repo.create(user=user)
