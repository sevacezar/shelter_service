from domain.users import UserRole, User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserNotFound, WrongPassword

class LoginUserUseCase:
    def __init__(self, user_repo: UserBaseRepository):
        self.user_repo = user_repo

    async def execute(
        self,
        email: str,
        password: str,
    ) -> User:
        user: User | None = await self.user_repo.get_by_email(email=email)
        if not user:
            raise UserNotFound('User with this email not found')

        if user.check_password(plain_password=password):
            return user
        else:
            raise WrongPassword('Wrong pasword!')
