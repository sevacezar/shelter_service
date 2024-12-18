from dataclasses import replace
from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.animal_views import AnimalView
from domain.animals import Animal
from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_base_repo import AnimalBaseRepository
from repositories.base.animal_view_base_repo import AnimalViewBaseRepository
from use_cases.views.create_view import CreateAnimalViewUseCase
from use_cases.exceptions import AnimalNotFound


async def test_create_view_use_case_success(
        not_admin_user: User,
        animal: Animal,
    ):
    user_id: str = not_admin_user.id
    animal_id: str = animal.id

    view_to_create: AnimalView = AnimalView(
        animal_id=animal_id,
        user_id=user_id,
    )
    created_view: AnimalView = replace(view_to_create, id=str(uuid4()))

    mock_animal_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)
    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_animal_repo.get_by_id.return_value = animal
    mock_user_repo.get_by_id.return_value = not_admin_user
    mock_animal_view_repo.create.return_value = created_view

    use_case: CreateAnimalViewUseCase = CreateAnimalViewUseCase(
        user_repo=mock_user_repo,
        animal_repo=mock_animal_repo,
        views_repo=mock_animal_view_repo,
    )
    res: AnimalView = await use_case.execute(
        animal_id=animal_id,
        user_id=user_id,
    )
    assert res == created_view
    mock_animal_repo.get_by_id.assert_called_once_with(id=animal_id)
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_view_repo.create.assert_called_once_with(view=view_to_create)

async def test_create_view_use_case_no_user(
        animal: Animal,
    ):
    animal_id: str = animal.id

    view_to_create: AnimalView = AnimalView(
        animal_id=animal_id,
    )
    created_view: AnimalView = replace(view_to_create, id=str(uuid4()))

    mock_animal_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)
    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_animal_repo.get_by_id.return_value = animal
    mock_animal_view_repo.create.return_value = created_view

    use_case: CreateAnimalViewUseCase = CreateAnimalViewUseCase(
        user_repo=mock_user_repo,
        animal_repo=mock_animal_repo,
        views_repo=mock_animal_view_repo,
    )
    res: AnimalView = await use_case.execute(
        animal_id=animal_id,
    )
    assert res == created_view
    mock_animal_repo.get_by_id.assert_called_once_with(id=animal_id)
    mock_user_repo.get_by_id.assert_not_called()
    mock_animal_view_repo.create.assert_called_once_with(view=view_to_create)

async def test_create_view_use_case_animal_not_found(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    animal_id: str = uuid4()

    mock_animal_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)
    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_view_repo: MagicMock = MagicMock(spec=AnimalViewBaseRepository)

    mock_animal_repo.get_by_id.return_value = None
    use_case: CreateAnimalViewUseCase = CreateAnimalViewUseCase(
        user_repo=mock_user_repo,
        animal_repo=mock_animal_repo,
        views_repo=mock_animal_view_repo,
    )
    with pytest.raises(AnimalNotFound):
        res: AnimalView = await use_case.execute(
            animal_id=animal_id,
            user_id=user_id,
        )
    mock_animal_repo.get_by_id.assert_called_once_with(id=animal_id)
    mock_user_repo.get_by_id.assert_not_called()
    mock_animal_view_repo.create.assert_not_called()
