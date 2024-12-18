from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.animal_views import AnimalView
from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository
from use_cases.views.get_all_views import GetAllAnimalViewsUseCase


async def test_get_all_views_use_case_success(
        admin: User,
    ):
    user_id: str = admin.id
    offset: int = 3
    limit: int = 2
    available_roles: list[str] = ['admin']

    views: list[AnimalView] = [
        AnimalView(
            animal_id=str(uuid4()),
            user_id=str(uuid4()),
        ),
        AnimalView(
            animal_id=str(uuid4()),
            user_id=str(uuid4()),
        ),
    ]
    
    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_animal_view_repo.get_all.return_value = views

    use_case: GetAllAnimalViewsUseCase = GetAllAnimalViewsUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    res: AnimalView = await use_case.execute(
        user_id=user_id,
        offset=offset,
        limit=limit,
    )
    assert res == views
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.get_all.assert_called_once_with(offset=offset, limit=limit)

async def test_get_all_views_use_case_not_admin_error(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    offset: int = 3
    limit: int = 2
    available_roles: list[str] = ['admin']
    
    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user

    use_case: GetAllAnimalViewsUseCase = GetAllAnimalViewsUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: AnimalView = await use_case.execute(
            user_id=user_id,
            offset=offset,
            limit=limit,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.get_all.assert_not_called()

async def test_get_all_views_use_case_user_not_found_error(
    ):
    user_id: str = str(uuid4())
    offset: int = 3
    limit: int = 2
    available_roles: list[str] = ['admin']
    
    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = None

    use_case: GetAllAnimalViewsUseCase = GetAllAnimalViewsUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: AnimalView = await use_case.execute(
            user_id=user_id,
            offset=offset,
            limit=limit,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.get_all.assert_not_called()
