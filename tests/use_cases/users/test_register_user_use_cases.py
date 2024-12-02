from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserAlreadyExists
from use_cases.users.register_user import RegisterUserUseCase

async def test_user_register_use_case_success():
    first_name: str = 'Jojn'
    second_name: str = 'Test'
    email: str = 'john@gmail.com'
    phone: str = '+79129129129'
    hashed_password: str = 'password_hashed'

    created_user_without_id: User = User(
        first_name=first_name,
        second_name=second_name,
        email=email,
        phone=phone,
        hashed_password=hashed_password,
    )
    created_user_with_id: User = User(
        first_name=first_name,
        second_name=second_name,
        email=email,
        phone=phone,
        hashed_password=hashed_password,
        id=uuid4(),
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_email.return_value = None
    mock_repo.create.return_value = created_user_with_id

    use_case: RegisterUserUseCase = RegisterUserUseCase(user_repo=mock_repo)
    res_user: User = await use_case.execute(
        first_name=first_name,
        second_name=second_name,
        email=email,
        phone=phone,
        hashed_password=hashed_password,
    )
    assert res_user.id == created_user_with_id.id
    assert res_user.first_name == first_name
    assert res_user.second_name == second_name
    assert res_user.email == email
    assert res_user.hashed_password == hashed_password
    assert res_user.role == 'user'
    mock_repo.get_by_email.assert_called_once_with(email=email)
    mock_repo.create.assert_called_once_with(user=created_user_without_id)

async def test_user_register_use_case_already_exists():
    first_name: str = 'Jojn'
    second_name: str = 'Test'
    email: str = 'john@gmail.com'
    phone: str = '+79129129129'
    hashed_password: str = 'password_hashed'

    created_user_with_id: User = User(
        first_name=first_name,
        second_name=second_name,
        email=email,
        phone=phone,
        hashed_password=hashed_password,
        id=uuid4(),
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_email.return_value = created_user_with_id

    use_case: RegisterUserUseCase = RegisterUserUseCase(user_repo=mock_repo)
    with pytest.raises(UserAlreadyExists):
        res_user: User = await use_case.execute(
            first_name=first_name,
            second_name=second_name,
            email=email,
            phone=phone,
            hashed_password=hashed_password,
        )

    mock_repo.get_by_email.assert_called_once_with(email=email)
    mock_repo.create.assert_not_called
