from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.users import User, UserRole
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.users.delete_user import DeleteUserUseCase

async def test_user_delete_test_case_success():
    cur_user_id = uuid4()
    deleted_user_email = 'deleted_user@mail.ru'

    cur_user: User = User(
        first_name='Poul',
        second_name='Black',
        email='admin@mail.ru',
        phone='+77777777777',
        hashed_password='hashed_password',
        role=UserRole.ADMIN.value,
        id=cur_user_id,
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.return_value = cur_user
    mock_repo.delete_by_email.return_value = None
    
    use_case: DeleteUserUseCase = DeleteUserUseCase(user_repo=mock_repo)
    res = await use_case.execute(
        admin_id=cur_user_id,
        deleted_user_email=deleted_user_email,
    )
    assert res is None
    mock_repo.get_by_id.assert_called_once_with(id=cur_user_id)
    mock_repo.delete_by_email.assert_called_once_with(email=deleted_user_email)

async def test_user_delete_test_case_permission_error():
    cur_user_id = uuid4()
    deleted_user_email = 'deleted_user@mail.ru'

    cur_user: User = User(
        first_name='Poul',
        second_name='Black',
        email='admin@mail.ru',
        phone='+77777777777',
        hashed_password='hashed_password',
        role=UserRole.USER.value,
        id=cur_user_id,
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.return_value = cur_user
    
    use_case: DeleteUserUseCase = DeleteUserUseCase(user_repo=mock_repo)
    with pytest.raises(PermissionError):
        res = await use_case.execute(
            admin_id=cur_user_id,
            deleted_user_email=deleted_user_email,
        )
    mock_repo.get_by_id.assert_called_once_with(id=cur_user_id)
    mock_repo.delete_by_email.assert_not_called()

