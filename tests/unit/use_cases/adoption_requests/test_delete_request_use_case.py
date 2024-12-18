from dataclasses import replace
from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.adoption_requests import AdoptionRequest
from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository
from use_cases.adoption_requests.delete_request import DeleteRequestUseCase
from use_cases.exceptions import AdoptionRequestNotFound


async def test_delete_request_use_case_success(
        admin: User,
    ):
    user_id: str = admin.id
    request_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    request: AdoptionRequest = AdoptionRequest(
        user_id=user_id,
        animal_id=uuid4(),
        id=request_id,
    )

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_adoption_request_repo.get_by_id.return_value = request
    mock_adoption_request_repo.delete.return_value = None

    use_case: DeleteRequestUseCase = DeleteRequestUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
    )
    res = await use_case.execute(
        user_id=user_id,
        request_id=request_id,
    )
    assert res is None
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.get_by_id.assert_called_once_with(id=request_id)
    mock_adoption_request_repo.delete.assert_called_once_with(request=request)

async def test_delete_request_use_case_user_not_admin(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    request_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user

    use_case: DeleteRequestUseCase = DeleteRequestUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
    )

    with pytest.raises(PermissionError):
        res = await use_case.execute(
            user_id=user_id,
            request_id=request_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.get_by_id.assert_not_called()
    mock_adoption_request_repo.delete.assert_not_called()

async def test_delete_request_use_case_request_not_found(
        admin: User,
    ):
    user_id: str = admin.id
    request_id: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_adoption_request_repo.get_by_id.return_value = None

    use_case: DeleteRequestUseCase = DeleteRequestUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
    )
    with pytest.raises(AdoptionRequestNotFound):
        res = await use_case.execute(
            user_id=user_id,
            request_id=request_id,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.get_by_id.assert_called_once_with(id=request_id)
    mock_adoption_request_repo.delete.assert_not_called()
