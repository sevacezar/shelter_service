from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.animal_views import AnimalView
from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository
from use_cases.views.get_views_by_animal_id import GetViewsByAnimalIdUseCase


async def test_get_views_by_animal_id_use_case_success(
        admin: User,
    ):
    user_id: str = admin.id
    animal_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    views: AnimalView = [
        AnimalView(
            animal_id=animal_id,
            user_id=str(uuid4()),
        ),
        AnimalView(
            animal_id=animal_id,
            user_id=str(uuid4()),
        )
    ]

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_animal_view_repo.list_by_animal.return_value = views

    use_case: GetViewsByAnimalIdUseCase = GetViewsByAnimalIdUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    res: AnimalView = await use_case.execute(
        animal_id=animal_id,
        user_id=user_id,
    )
    assert res == views
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.list_by_animal.assert_called_once_with(animal_id=animal_id)

async def test_get_views_by_animal_id_use_case_not_admin_error(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    animal_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user

    use_case: GetViewsByAnimalIdUseCase = GetViewsByAnimalIdUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: AnimalView = await use_case.execute(
            animal_id=animal_id,
            user_id=user_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.list_by_animal.assert_not_called()

async def test_get_views_by_animal_id_use_case_user_not_found_error(
    ):
    user_id: str = str(uuid4())
    animal_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = None

    use_case: GetViewsByAnimalIdUseCase = GetViewsByAnimalIdUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: AnimalView = await use_case.execute(
            animal_id=animal_id,
            user_id=user_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.list_by_animal.assert_not_called()