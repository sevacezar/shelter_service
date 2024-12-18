from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.animal_views import AnimalView
from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository
from use_cases.views.get_views_by_user_id import GetViewsByUserIdUseCase


async def test_get_views_by_user_id_use_case_by_admin_success(
        admin: User,
    ):
    cur_user_id: str = admin.id
    target_user_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    views: AnimalView = [
        AnimalView(
            animal_id=str(uuid4()),
            user_id=target_user_id,
        ),
        AnimalView(
            animal_id=str(uuid4()),
            user_id=target_user_id,
        )
    ]

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_animal_view_repo.list_by_user.return_value = views

    use_case: GetViewsByUserIdUseCase = GetViewsByUserIdUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    res: AnimalView = await use_case.execute(
        cur_user_id=cur_user_id,
        target_user_id=target_user_id,
    )
    assert res == views
    mock_user_repo.get_by_id.assert_called_once_with(id=cur_user_id)
    mock_animal_view_repo.list_by_user.assert_called_once_with(user_id=target_user_id)

async def test_get_views_by_user_id_use_case_by_user_success(
        not_admin_user: User,
    ):
    cur_user_id: str = not_admin_user.id
    target_user_id: str = cur_user_id
    available_roles: list[str] = ['admin']

    views: AnimalView = [
        AnimalView(
            animal_id=str(uuid4()),
            user_id=target_user_id,
        ),
        AnimalView(
            animal_id=str(uuid4()),
            user_id=target_user_id,
        )
    ]

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user
    mock_animal_view_repo.list_by_user.return_value = views

    use_case: GetViewsByUserIdUseCase = GetViewsByUserIdUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    res: AnimalView = await use_case.execute(
        cur_user_id=cur_user_id,
        target_user_id=target_user_id,
    )
    assert res == views
    mock_user_repo.get_by_id.assert_called_once_with(id=cur_user_id)
    mock_animal_view_repo.list_by_user.assert_called_once_with(user_id=target_user_id)

async def test_get_views_by_user_id_use_case_foreign_user_error(
        not_admin_user: User,
    ):
    cur_user_id: str = not_admin_user.id
    target_user_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user

    use_case: GetViewsByUserIdUseCase = GetViewsByUserIdUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: AnimalView = await use_case.execute(
            cur_user_id=cur_user_id,
            target_user_id=target_user_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=cur_user_id)
    mock_animal_view_repo.list_by_user.assert_not_called()

async def test_get_views_by_user_id_use_case_user_nit_found_error(
    ):
    cur_user_id: str = str(uuid4())
    target_user_id: str = cur_user_id
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = None

    use_case: GetViewsByUserIdUseCase = GetViewsByUserIdUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: AnimalView = await use_case.execute(
            cur_user_id=cur_user_id,
            target_user_id=target_user_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=cur_user_id)
    mock_animal_view_repo.list_by_user.assert_not_called()