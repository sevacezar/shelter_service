from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserNotFound
from use_cases.users.get_user import GetUserByIdUseCase

async def test_get_user_test_case_success_admin():
    cur_user_id = uuid4()
    searched_user_id = uuid4()

    cur_user: User = User(
        first_name='Poul',
        second_name='Black',
        email='admin@mail.ru',
        phone='+77777777777',
        hashed_password='hashed_password',
        role='admin',
        id=cur_user_id,
    )

    searched_user: User = User(
        first_name='Searched',
        second_name='User',
        email='searched@mail.ru',
        phone='+888888888',
        hashed_password='hashed_password',
        id=searched_user_id,
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.side_effect = lambda id: {
        cur_user_id: cur_user,
        searched_user_id: searched_user,
    }.get(id)
    
    use_case: GetUserByIdUseCase = GetUserByIdUseCase(user_repo=mock_repo)
    res = await use_case.execute(
        cur_user_id=cur_user_id,
        searched_user_id=searched_user_id,
    )
    assert res == searched_user
    mock_repo.get_by_id.assert_any_call(id=cur_user_id)
    mock_repo.get_by_id.assert_any_call(id=searched_user_id)

async def test_get_user_test_case_success_user():
    cur_user_id = uuid4()
    searched_user_id = cur_user_id

    cur_user: User = User(
        first_name='Poul',
        second_name='Black',
        email='admin@mail.ru',
        phone='+77777777777',
        hashed_password='hashed_password',
        id=cur_user_id,
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.side_effect = lambda id: {
        cur_user_id: cur_user,
        searched_user_id: cur_user,
    }.get(id)
    
    use_case: GetUserByIdUseCase = GetUserByIdUseCase(user_repo=mock_repo)
    res = await use_case.execute(
        cur_user_id=cur_user_id,
        searched_user_id=searched_user_id,
    )
    assert res == cur_user
    mock_repo.get_by_id.assert_any_call(id=cur_user_id)
    mock_repo.get_by_id.assert_any_call(id=searched_user_id)

async def test_get_user_test_case_cur_user_not_found():
    cur_user_id = uuid4()
    searched_user_id = cur_user_id

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.return_value = None
    use_case: GetUserByIdUseCase = GetUserByIdUseCase(user_repo=mock_repo)
    with pytest.raises(UserNotFound):
        res = await use_case.execute(
            cur_user_id=cur_user_id,
            searched_user_id=searched_user_id,
        )
    mock_repo.get_by_id.assert_called_once_with(id=cur_user_id)

async def test_get_user_test_case_permission_error():
    cur_user_id = uuid4()
    searched_user_id = uuid4()

    cur_user: User = User(
        first_name='Poul',
        second_name='Black',
        email='admin@mail.ru',
        phone='+77777777777',
        hashed_password='hashed_password',
        id=cur_user_id,
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.return_value = cur_user
    use_case: GetUserByIdUseCase = GetUserByIdUseCase(user_repo=mock_repo)
    with pytest.raises(PermissionError):
        res = await use_case.execute(
            cur_user_id=cur_user_id,
            searched_user_id=searched_user_id,
        )
    mock_repo.get_by_id.assert_called_once_with(id=cur_user_id)
