from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.adoption_requests import AdoptionRequest
from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository
from use_cases.adoption_requests.get_by_animal_id import GetRequestsByAnimalIdUseCase


async def test_get_requests_by_animal_id_use_case_success(
        admin: User,
    ):
    user_id: str = admin.id
    animal_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    requests: list[AdoptionRequest] = [
        AdoptionRequest(
            user_id=str(uuid4()),
            animal_id=animal_id,
            status='approved',
            user_comment='Comment',
            id=str(uuid4()),
        ),
        AdoptionRequest(
            user_id=str(uuid4()),
            animal_id=animal_id,
            status='canceled',
            user_comment='Comment',
            id=str(uuid4()),
        ),
    ]

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_adoption_request_repo.list_by_animal.return_value = requests

    use_case: GetRequestsByAnimalIdUseCase = GetRequestsByAnimalIdUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
    )
    res: list[AdoptionRequest] = await use_case.execute(
        user_id=user_id,
        animal_id=animal_id,
    )
    assert res == requests
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.list_by_animal.assert_called_once_with(animal_id=animal_id)

async def test_get_requests_by_animal_id_use_case_user_not_admin(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    animal_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user

    use_case: GetRequestsByAnimalIdUseCase = GetRequestsByAnimalIdUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: list[AdoptionRequest] = await use_case.execute(
            user_id=user_id,
            animal_id=animal_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.list_by_animal.assert_not_called()

async def test_get_requests_by_animal_id_use_case_user_not_found():
    user_id: str = str(uuid4())
    animal_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = None

    use_case: GetRequestsByAnimalIdUseCase = GetRequestsByAnimalIdUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: list[AdoptionRequest] = await use_case.execute(
            user_id=user_id,
            animal_id=animal_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.list_by_animal.assert_not_called()
