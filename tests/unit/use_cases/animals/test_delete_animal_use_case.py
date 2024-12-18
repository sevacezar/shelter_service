from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.users import User
from domain.animals import Animal
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_base_repo import AnimalBaseRepository
from use_cases.animals.delete_animal import DeleteAnimalByIdUseCase
from use_cases.exceptions import AnimalNotFound

async def test_delete_animal_use_case_success(admin: User, animal: Animal):
    user_id: str = str(admin.id)
    animal_id: str = str(animal.id)
    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    animal_mock_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)

    user_mock_repo.get_by_id.return_value = admin
    animal_mock_repo.get_by_id.return_value = animal

    use_case: DeleteAnimalByIdUseCase = DeleteAnimalByIdUseCase(
            animal_repo=animal_mock_repo,
            user_repo=user_mock_repo,
            available_roles=available_roles,
    )
    res: Animal = await use_case.execute(
            user_id=user_id,
            animal_id=animal_id,
    )
    assert res is None
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    animal_mock_repo.get_by_id.assert_called_once_with(id=animal_id)
    animal_mock_repo.delete.assert_called_once_with(animal=animal)

async def test_delete_animal_use_case_user_not_admin(not_admin_user: User):
    user_id: str = str(not_admin_user.id)
    animal_id: str = str(uuid4())
    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    animal_mock_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)

    user_mock_repo.get_by_id.return_value = not_admin_user

    use_case: DeleteAnimalByIdUseCase = DeleteAnimalByIdUseCase(
            animal_repo=animal_mock_repo,
            user_repo=user_mock_repo,
            available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: Animal = await use_case.execute(
                user_id=user_id,
                animal_id=animal_id,
        )

    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    animal_mock_repo.get_by_id.assert_not_called()
    animal_mock_repo.delete.assert_not_called()

async def test_delete_animal_use_case_user_not_found():
    user_id: str = str(uuid4())
    animal_id: str = str(uuid4())
    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    animal_mock_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)

    user_mock_repo.get_by_id.return_value = None

    use_case: DeleteAnimalByIdUseCase = DeleteAnimalByIdUseCase(
            animal_repo=animal_mock_repo,
            user_repo=user_mock_repo,
            available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: Animal = await use_case.execute(
                user_id=user_id,
                animal_id=animal_id,
        )

    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    animal_mock_repo.get_by_id.assert_not_called()
    animal_mock_repo.delete.assert_not_called()

async def test_delete_animal_use_case_animal_not_found(admin: User):
    user_id: str = str(admin.id)
    animal_id: str = str(uuid4())
    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    animal_mock_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)

    user_mock_repo.get_by_id.return_value = admin
    animal_mock_repo.get_by_id.return_value = None

    use_case: DeleteAnimalByIdUseCase = DeleteAnimalByIdUseCase(
            animal_repo=animal_mock_repo,
            user_repo=user_mock_repo,
            available_roles=available_roles,
    )
    with pytest.raises(AnimalNotFound):
        res: Animal = await use_case.execute(
                user_id=user_id,
                animal_id=animal_id,
        )
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    animal_mock_repo.get_by_id.assert_called_once_with(id=animal_id)
    animal_mock_repo.delete.assert_not_called()