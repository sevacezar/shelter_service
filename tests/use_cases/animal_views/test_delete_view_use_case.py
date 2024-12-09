from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.animal_views import AnimalView
from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository
from use_cases.views.delete_view import DeleteAnimalViewUseCase
from use_cases.exceptions import AnimalViewNotFound


async def test_delete_view_use_case_success(
        admin: User,
    ):
    user_id: str = admin.id
    view_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    view_to_delete: AnimalView = AnimalView(
        animal_id=str(uuid4()),
        user_id=str(uuid4()),
    )

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_animal_view_repo.get_by_id.return_value = view_to_delete
    mock_animal_view_repo.delete.return_value = None

    use_case: DeleteAnimalViewUseCase = DeleteAnimalViewUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    res = await use_case.execute(
        user_id=user_id,
        view_id=view_id,
    )
    assert res is None
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.get_by_id.assert_called_once_with(id=view_id)
    mock_animal_view_repo.delete.assert_called_once_with(view=view_to_delete)


async def test_delete_view_use_case_not_admin_error(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    view_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user

    use_case: DeleteAnimalViewUseCase = DeleteAnimalViewUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res = await use_case.execute(
            user_id=user_id,
            view_id=view_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.get_by_id.assert_not_called()
    mock_animal_view_repo.delete.assert_not_called()

async def test_delete_view_use_case_not_found_error(
    ):
    user_id: str = str(uuid4())
    view_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = None

    use_case: DeleteAnimalViewUseCase = DeleteAnimalViewUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res = await use_case.execute(
            user_id=user_id,
            view_id=view_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.get_by_id.assert_not_called()
    mock_animal_view_repo.delete.assert_not_called()

async def test_delete_view_use_case_animal_view_not_found_error(
        admin: User,
    ):
    user_id: str = admin.id
    view_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_animal_view_repo.get_by_id.return_value = None

    use_case: DeleteAnimalViewUseCase = DeleteAnimalViewUseCase(
        user_repo=mock_user_repo,
        views_repo=mock_animal_view_repo,
        available_roles=available_roles,
    )
    with pytest.raises(AnimalViewNotFound):
        res = await use_case.execute(
            user_id=user_id,
            view_id=view_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.get_by_id.assert_called_once_with(id=view_id)
    mock_animal_view_repo.delete.assert_not_called()

