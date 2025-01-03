from domain.users import UserRole, User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserAlreadyExists

class RegisterUserUseCase:
    def __init__(self, user_repo: UserBaseRepository):
        self.user_repo = user_repo
    
    async def execute(
        self,
        first_name: str,
        second_name: str,
        email: str,
        phone: str,
        password: str,
        role: UserRole = UserRole.USER.value,
    ) -> User:
        existing_user: User | None = await self.user_repo.get_by_email(email=email)
        if existing_user:
            raise UserAlreadyExists('User with this email already exists')
        
        hashed_password: str = User.get_password_hash(password=password)
        user = User(
            first_name=first_name,
            second_name=second_name,
            email=email,
            phone=phone,
            hashed_password=hashed_password,
            role=role,
        )
        return await self.user_repo.create(user=user)
    