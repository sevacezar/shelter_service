from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.users import User
from domain.animals import Animal
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_base_repo import AnimalBaseRepository
from use_cases.animals.create_animal import CreateAnimalUseCase

async def test_animal_create_use_case_success(admin: User):
        user_id: str = str(admin.id)
        name: str = 'Daysy'
        color: str = 'white'
        size: int = 'medium'
        birth_date: datetime = datetime(2020, 1, 10, tzinfo=timezone.utc)
        in_shelter_at: datetime = datetime(2021, 1, 10, tzinfo=timezone.utc)
        description: str = 'Funny dog'

        available_roles: list = ['admin']

        animal_to_create: Animal = Animal(
            name=name,
            color=color,
            size=size,
            birth_date=birth_date,
            in_shelter_at=in_shelter_at,
            description=description,
        )

        created_animal: Animal = Animal(
            name=name,
            color=color,
            size=size,
            birth_date=birth_date,
            in_shelter_at=in_shelter_at,
            description=description,
            id=str(uuid4()),
        )

        user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
        animal_mock_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)

        user_mock_repo.get_by_id.return_value = admin
        animal_mock_repo.create.return_value = created_animal

        use_case: CreateAnimalUseCase = CreateAnimalUseCase(
             animal_repo=animal_mock_repo,
             user_repo=user_mock_repo,
             available_roles=available_roles,
        )
        res: Animal = await use_case.execute(
             user_id=user_id,
             name=name,
             color=color,
             size=size,
             birth_date=birth_date,
             in_shelter_at=in_shelter_at,
             description=description,
        )
        assert res == created_animal
        user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
        animal_mock_repo.create.assert_called_once_with(animal=animal_to_create)



async def test_animal_create_use_case_user_not_admin(not_admin_user: User):
        user_id: str = str(not_admin_user.id)
        name: str = 'Daysy'
        color: str = 'white'
        birth_date: datetime = datetime(2020, 1, 10, tzinfo=timezone.utc)
        in_shelter_at: datetime = datetime(2021, 1, 10, tzinfo=timezone.utc)
        description: str = 'Funny dog'

        available_roles: list = ['admin']

        animal_to_create: Animal = Animal(
            name=name,
            color=color,
            birth_date=birth_date,
            in_shelter_at=in_shelter_at,
            description=description,
        )

        user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
        animal_mock_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)

        user_mock_repo.get_by_id.return_value = not_admin_user
        use_case: CreateAnimalUseCase = CreateAnimalUseCase(
             animal_repo=animal_mock_repo,
             user_repo=user_mock_repo,
             available_roles=available_roles,
        )
        with pytest.raises(PermissionError):
            res: Animal = await use_case.execute(
                user_id=user_id,
                name=name,
                color=color,
                birth_date=birth_date,
                in_shelter_at=in_shelter_at,
                description=description,
            )
        user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
        animal_mock_repo.create.assert_not_called()


async def test_animal_create_use_case_user_not_found():
        user_id: str = str(uuid4())
        name: str = 'Daysy'
        color: str = 'white'
        birth_date: datetime = datetime(2020, 1, 10, tzinfo=timezone.utc)
        in_shelter_at: datetime = datetime(2021, 1, 10, tzinfo=timezone.utc)
        description: str = 'Funny dog'

        available_roles: list = ['admin']

        user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
        animal_mock_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)

        user_mock_repo.get_by_id.return_value = None
        use_case: CreateAnimalUseCase = CreateAnimalUseCase(
             animal_repo=animal_mock_repo,
             user_repo=user_mock_repo,
             available_roles=available_roles,
        )
        with pytest.raises(PermissionError):
            res: Animal = await use_case.execute(
                user_id=user_id,
                name=name,
                color=color,
                birth_date=birth_date,
                in_shelter_at=in_shelter_at,
                description=description,
            )
        user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
        animal_mock_repo.create.assert_not_called()