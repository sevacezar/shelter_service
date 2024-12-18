from dataclasses import replace
from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.adoption_requests import AdoptionRequest
from domain.animals import Animal
from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.animal_base_repo import AnimalBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository
from use_cases.adoption_requests.create_request import CreateRequestUseCase
from use_cases.exceptions import AnimalNotFound


async def test_create_request_use_case_success(
        not_admin_user: User,
        animal: Animal,
    ):
    user_id: str = not_admin_user.id
    animal_id: str = animal.id
    comment: str = 'Some comment'

    request_to_create: AdoptionRequest = AdoptionRequest(
        user_id=user_id,
        animal_id=animal_id,
        user_comment=comment,
    )
    created_request: AdoptionRequest = replace(request_to_create, id=str(uuid4()))

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user
    mock_animal_repo.get_by_id.return_value = animal
    mock_adoption_request_repo.create.return_value = created_request

    use_case: CreateRequestUseCase = CreateRequestUseCase(
        user_repo=mock_user_repo,
        animal_repo=mock_animal_repo,
        adoption_requests_repo=mock_adoption_request_repo,
    )
    res: AdoptionRequest = await use_case.execute(
        user_id=user_id,
        animal_id=animal_id,
        comment=comment,
    )
    assert res == created_request
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_repo.get_by_id.assert_called_once_with(id=animal_id)
    mock_adoption_request_repo.create.assert_called_once_with(request=request_to_create)

async def test_create_request_use_case_user_not_found(
        animal: Animal,
    ):
    user_id: str = str(uuid4())
    animal_id: str = animal.id
    comment: str = 'Some comment'

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = None

    use_case: CreateRequestUseCase = CreateRequestUseCase(
        user_repo=mock_user_repo,
        animal_repo=mock_animal_repo,
        adoption_requests_repo=mock_adoption_request_repo,
    )
    with pytest.raises(PermissionError):
        res: AdoptionRequest = await use_case.execute(
            user_id=user_id,
            animal_id=animal_id,
            comment=comment,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_repo.get_by_id.assert_not_called()
    mock_adoption_request_repo.create.assert_not_called()

async def test_create_request_use_case_animal_not_found(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    animal_id: str = str(uuid4())
    comment: str = 'Some comment'

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_animal_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user
    mock_animal_repo.get_by_id.return_value = None

    use_case: CreateRequestUseCase = CreateRequestUseCase(
        user_repo=mock_user_repo,
        animal_repo=mock_animal_repo,
        adoption_requests_repo=mock_adoption_request_repo,
    )
    with pytest.raises(AnimalNotFound):
        res: AdoptionRequest = await use_case.execute(
            user_id=user_id,
            animal_id=animal_id,
            comment=comment,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_animal_repo.get_by_id.assert_called_once_with(id=animal_id)
    mock_adoption_request_repo.create.assert_not_called()
    