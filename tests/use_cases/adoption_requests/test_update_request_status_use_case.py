from dataclasses import replace
from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.adoption_requests import AdoptionRequest
from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository
from use_cases.adoption_requests.update_status import UpdateStatusRequestUseCase
from use_cases.exceptions import AdoptionRequestNotFound


async def test_update_status_request_by_admin_success(
        admin: User,
    ):
    user_id: str = admin.id
    request_id: str = str(uuid4())
    new_status: str = 'rejected'
    available_roles: list[str] = ['admin']
    available_statuses_for_users: list[str] = ['cancelled']

    request_to_update: AdoptionRequest = AdoptionRequest(
        user_id=str(uuid4()),
        animal_id=str(uuid4()),
        status='pending',
        user_comment='Comment',
        id=request_id,
    )
    updated_request: AdoptionRequest = replace(request_to_update, status=new_status)

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_adoption_request_repo.get_by_id.return_value = request_to_update
    mock_adoption_request_repo.update_status.return_value = updated_request

    use_case: UpdateStatusRequestUseCase = UpdateStatusRequestUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
        available_statuses_for_users=available_statuses_for_users,
    )

    res: AdoptionRequest = await use_case.execute(
        user_id=user_id,
        request_id=request_id,
        new_status=new_status,
    )
    assert res == updated_request
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.get_by_id.assert_called_once_with(id=request_id)
    mock_adoption_request_repo.update_status.assert_called_once_with(request=request_to_update, new_status=new_status)

async def test_update_status_request_by_user_success(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    request_id: str = str(uuid4())
    new_status: str = 'cancelled'
    available_roles: list[str] = ['admin']
    available_statuses_for_users: list[str] = ['cancelled']

    request_to_update: AdoptionRequest = AdoptionRequest(
        user_id=user_id,
        animal_id=str(uuid4()),
        status='pending',
        user_comment='Comment',
        id=request_id,
    )
    updated_request: AdoptionRequest = replace(request_to_update, status=new_status)

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user
    mock_adoption_request_repo.get_by_id.return_value = request_to_update
    mock_adoption_request_repo.update_status.return_value = updated_request

    use_case: UpdateStatusRequestUseCase = UpdateStatusRequestUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
        available_statuses_for_users=available_statuses_for_users,
    )

    res: AdoptionRequest = await use_case.execute(
        user_id=user_id,
        request_id=request_id,
        new_status=new_status,
    )
    assert res == updated_request
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.get_by_id.assert_called_once_with(id=request_id)
    mock_adoption_request_repo.update_status.assert_called_once_with(request=request_to_update, new_status=new_status)

async def test_update_status_request_user_not_found_error(
    ):
    user_id: str = str(uuid4())
    request_id: str = str(uuid4())
    new_status: str = 'cancelled'
    available_roles: list[str] = ['admin']
    available_statuses_for_users: list[str] = ['cancelled']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = None

    use_case: UpdateStatusRequestUseCase = UpdateStatusRequestUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
        available_statuses_for_users=available_statuses_for_users,
    )
    with pytest.raises(PermissionError):
        res: AdoptionRequest = await use_case.execute(
            user_id=user_id,
            request_id=request_id,
            new_status=new_status,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.get_by_id.assert_not_called()
    mock_adoption_request_repo.update_status.assert_not_called()

async def test_update_status_request_by_admin_success(
        admin: User,
    ):
    user_id: str = admin.id
    request_id: str = str(uuid4())
    new_status: str = 'rejected'
    available_roles: list[str] = ['admin']
    available_statuses_for_users: list[str] = ['cancelled']

    request_to_update: AdoptionRequest = AdoptionRequest(
        user_id=str(uuid4()),
        animal_id=str(uuid4()),
        status='pending',
        user_comment='Comment',
        id=request_id,
    )
    updated_request: AdoptionRequest = replace(request_to_update, status=new_status)

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_adoption_request_repo.get_by_id.return_value = request_to_update
    mock_adoption_request_repo.update_status.return_value = updated_request

    use_case: UpdateStatusRequestUseCase = UpdateStatusRequestUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
        available_statuses_for_users=available_statuses_for_users,
    )

    res: AdoptionRequest = await use_case.execute(
        user_id=user_id,
        request_id=request_id,
        new_status=new_status,
    )
    assert res == updated_request
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.get_by_id.assert_called_once_with(id=request_id)
    mock_adoption_request_repo.update_status.assert_called_once_with(request=request_to_update, new_status=new_status)

async def test_update_status_request_by_user_invalid_status_error(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    request_id: str = str(uuid4())
    new_status: str = 'approved'
    available_roles: list[str] = ['admin']
    available_statuses_for_users: list[str] = ['cancelled']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user

    use_case: UpdateStatusRequestUseCase = UpdateStatusRequestUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
        available_statuses_for_users=available_statuses_for_users,
    )
    with pytest.raises(PermissionError):
        res: AdoptionRequest = await use_case.execute(
            user_id=user_id,
            request_id=request_id,
            new_status=new_status,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.get_by_id.assert_not_called()
    mock_adoption_request_repo.update_status.assert_not_called()

async def test_update_status_request_not_found_error(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    request_id: str = str(uuid4())
    new_status: str = 'cancelled'
    available_roles: list[str] = ['admin']
    available_statuses_for_users: list[str] = ['cancelled']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user
    mock_adoption_request_repo.get_by_id.return_value = None

    use_case: UpdateStatusRequestUseCase = UpdateStatusRequestUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
        available_statuses_for_users=available_statuses_for_users,
    )
    with pytest.raises(AdoptionRequestNotFound):
        res: AdoptionRequest = await use_case.execute(
            user_id=user_id,
            request_id=request_id,
            new_status=new_status,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.get_by_id.assert_called_once_with(id=request_id)
    mock_adoption_request_repo.update_status.assert_not_called()


async def test_update_status_request_by_user_foreigh_request_error(
        not_admin_user: User,
    ):
    user_id: str = not_admin_user.id
    request_id: str = str(uuid4())
    new_status: str = 'cancelled'
    available_roles: list[str] = ['admin']
    available_statuses_for_users: list[str] = ['cancelled']

    request_to_update: AdoptionRequest = AdoptionRequest(
        user_id=str(uuid4()),
        animal_id=str(uuid4()),
        status='pending',
        user_comment='Comment',
        id=request_id,
    )

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user
    mock_adoption_request_repo.get_by_id.return_value = request_to_update

    use_case: UpdateStatusRequestUseCase = UpdateStatusRequestUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
        available_statuses_for_users=available_statuses_for_users,
    )
    with pytest.raises(PermissionError):
        res: AdoptionRequest = await use_case.execute(
            user_id=user_id,
            request_id=request_id,
            new_status=new_status,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=user_id)
    mock_adoption_request_repo.get_by_id.assert_called_once_with(id=request_id)
    mock_adoption_request_repo.update_status.assert_not_called()


