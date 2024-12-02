from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserNotFound
from use_cases.users.update_user import UpdateUserByIdUseCase


async def test_update_user_use_case_success_admin():
    cur_user_id = uuid4()
    updated_user_id = uuid4()
    available_roles: list[str] = ['admin']
    updated_params: dict = {
        'role': 'admin',
    }

    cur_user: User = User(
        first_name='Poul',
        second_name='Black',
        email='admin@mail.ru',
        phone='+77777777777',
        hashed_password='hashed_password',
        role='admin',
        id=cur_user_id,
    )

    user_to_update: User = User(
        first_name='John',
        second_name='Smith',
        email='john@mail.ru',
        phone='+79129999999',
        hashed_password='hashed_password',
        id=updated_user_id,
    )

    updated_user: User = User(
        first_name='John',
        second_name='Smith',
        email='john@mail.ru',
        phone='+79129999999',
        hashed_password='hashed_password',
        id=updated_user_id,
        role='admin',
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.side_effect = lambda id: {
        cur_user_id: cur_user,
        updated_user_id: user_to_update,
    }.get(id)
    mock_repo.update.return_value = updated_user

    use_case: UpdateUserByIdUseCase = UpdateUserByIdUseCase(
        user_repo=mock_repo,
        available_roles=available_roles,
    )
    res: User = await use_case.execute(
        cur_user_id=cur_user_id,
        updated_user_id=updated_user_id,
        updated_params=updated_params,
    )
    assert res == updated_user
    mock_repo.get_by_id.assert_any_call(id=cur_user_id)
    mock_repo.get_by_id.assert_any_call(id=updated_user_id)
    mock_repo.update.assert_called_once_with(
        user=user_to_update,
        updated_params=updated_params,
    )

async def test_update_user_use_case_success_user():
    cur_user_id = uuid4()
    updated_user_id = cur_user_id
    available_roles: list[str] = ['admin']

    updated_params: dict = {
        'first_name': 'Poul_',
        'second_name': 'Black_',
        'email': 'user_@mail.ru',
        'phone': '+77777777771',
        'hashed_password': 'hashed_password_',
    }

    cur_user: User = User(
        first_name='Poul',
        second_name='Black',
        email='user@mail.ru',
        phone='+77777777777',
        hashed_password='hashed_password',
        id=cur_user_id,
    )

    user_to_update: User = cur_user

    updated_user: User = User(
        first_name=updated_params.get('first_name'),
        second_name=updated_params.get('second_name'),
        email=updated_params.get('email'),
        phone=updated_params.get('phone'),
        hashed_password=updated_params.get('hashed_password'),
        id=updated_user_id,
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.side_effect = lambda id: {
        cur_user_id: cur_user,
        updated_user_id: user_to_update,
    }.get(id)
    mock_repo.update.return_value = updated_user

    use_case: UpdateUserByIdUseCase = UpdateUserByIdUseCase(
        user_repo=mock_repo,
        available_roles=available_roles,
    )
    res: User = await use_case.execute(
        cur_user_id=cur_user_id,
        updated_user_id=updated_user_id,
        updated_params=updated_params,
    )
    assert res == updated_user
    mock_repo.get_by_id.assert_any_call(id=cur_user_id)
    mock_repo.get_by_id.assert_any_call(id=updated_user_id)
    mock_repo.update.assert_called_once_with(
        user=user_to_update,
        updated_params=updated_params,
    )

async def test_update_user_use_case_cur_user_not_found():
    cur_user_id = uuid4()
    updated_user_id = cur_user_id
    available_roles: list[str] = ['admin']

    updated_params: dict = {
        'first_name': 'Poul_',
        'second_name': 'Black_',
        'email': 'user_@mail.ru',
        'phone': '+77777777771',
        'hashed_password': 'hashed_password_',
    }

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.return_value = None
    use_case: UpdateUserByIdUseCase = UpdateUserByIdUseCase(
        user_repo=mock_repo,
        available_roles=available_roles,
    )

    with pytest.raises(UserNotFound):
        res: User = await use_case.execute(
            cur_user_id=cur_user_id,
            updated_user_id=updated_user_id,
            updated_params=updated_params,
        )

    mock_repo.get_by_id.assert_called_once_with(id=cur_user_id)

async def test_update_user_use_case_permission_error():
    cur_user_id = uuid4()
    updated_user_id = uuid4()
    available_roles: list[str] = ['admin']

    updated_params: dict = {
        'first_name': 'Poul_',
        'second_name': 'Black_',
        'email': 'user_@mail.ru',
        'phone': '+77777777771',
        'hashed_password': 'hashed_password_',
    }

    cur_user: User = User(
        first_name='John',
        second_name='Smith',
        email='jony@mail.ru',
        phone='+77777777712',
        hashed_password='hashed_password',
        id=cur_user_id,
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.return_value = cur_user

    use_case: UpdateUserByIdUseCase = UpdateUserByIdUseCase(
        user_repo=mock_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: User = await use_case.execute(
            cur_user_id=cur_user_id,
            updated_user_id=updated_user_id,
            updated_params=updated_params,
        )
    mock_repo.get_by_id.assert_called_once_with(id=cur_user_id)

async def test_update_user_use_case_updated_user_not_found():
    cur_user_id = uuid4()
    updated_user_id = uuid4()
    available_roles: list[str] = ['admin']
    updated_params: dict = {
        'first_name': 'Edward',
    }

    cur_user: User = User(
        first_name='Poul',
        second_name='Black',
        email='admin@mail.ru',
        phone='+77777777777',
        hashed_password='hashed_password',
        role='admin',
        id=cur_user_id,
    )

    mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_repo.get_by_id.side_effect = lambda id: {
        cur_user_id: cur_user,
        updated_user_id: None,
    }.get(id)

    use_case: UpdateUserByIdUseCase = UpdateUserByIdUseCase(
        user_repo=mock_repo,
        available_roles=available_roles,
    )
    with pytest.raises(UserNotFound):
        res: User = await use_case.execute(
            cur_user_id=cur_user_id,
            updated_user_id=updated_user_id,
            updated_params=updated_params,
        )
    mock_repo.get_by_id.assert_any_call(id=cur_user_id)
    mock_repo.get_by_id.assert_any_call(id=updated_user_id)
