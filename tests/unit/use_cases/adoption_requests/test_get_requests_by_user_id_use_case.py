from unittest.mock import MagicMock
from uuid import uuid4
import pytest

from domain.adoption_requests import AdoptionRequest
from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from repositories.base.adoption_request_base_repo import AdoptionRequestBaseRepository
from use_cases.adoption_requests.get_by_user_id import GetRequestsByUserIdUseCase


async def test_get_requests_by_user_id_use_case_admin_success(
        admin: User,
    ):
    cur_user_id: str = admin.id
    user_id_to_search: str = str(uuid4())
    available_roles: list[str] = ['admin']

    requests: list[AdoptionRequest] = [
        AdoptionRequest(
            user_id=user_id_to_search,
            animal_id=str(uuid4()),
            status='approved',
            user_comment='Comment',
            id=str(uuid4()),
        ),
        AdoptionRequest(
            user_id=user_id_to_search,
            animal_id=str(uuid4()),
            status='canceled',
            user_comment='Comment',
            id=str(uuid4()),
        ),
    ]

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = admin
    mock_adoption_request_repo.list_by_user.return_value = requests

    use_case: GetRequestsByUserIdUseCase = GetRequestsByUserIdUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
    )

    res: list[AdoptionRequest] = await use_case.execute(
        cur_user_id=cur_user_id,
        user_id_to_search=user_id_to_search,
    )
    assert res == requests
    mock_user_repo.get_by_id.assert_called_once_with(id=cur_user_id)
    mock_adoption_request_repo.list_by_user.assert_called_once_with(user_id=user_id_to_search)

async def test_get_requests_by_user_id_use_case_user_not_admin_success(
        not_admin_user: User,
    ):
    cur_user_id: str = not_admin_user.id
    user_id_to_search: str = cur_user_id
    available_roles: list[str] = ['admin']

    requests: list[AdoptionRequest] = [
        AdoptionRequest(
            user_id=user_id_to_search,
            animal_id=str(uuid4()),
            status='approved',
            user_comment='Comment',
            id=str(uuid4()),
        ),
        AdoptionRequest(
            user_id=user_id_to_search,
            animal_id=str(uuid4()),
            status='canceled',
            user_comment='Comment',
            id=str(uuid4()),
        ),
    ]

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user
    mock_adoption_request_repo.list_by_user.return_value = requests

    use_case: GetRequestsByUserIdUseCase = GetRequestsByUserIdUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
    )
    res: list[AdoptionRequest] = await use_case.execute(
        cur_user_id=cur_user_id,
        user_id_to_search=user_id_to_search,
    )
    assert res == requests
    mock_user_repo.get_by_id.assert_called_once_with(id=cur_user_id)
    mock_adoption_request_repo.list_by_user.assert_called_once_with(user_id=user_id_to_search)

async def test_get_requests_by_user_id_use_case_user_not_admin_error(
        not_admin_user: User,
    ):
    cur_user_id: str = not_admin_user.id
    user_id_to_search: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = not_admin_user

    use_case: GetRequestsByUserIdUseCase = GetRequestsByUserIdUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: list[AdoptionRequest] = await use_case.execute(
            cur_user_id=cur_user_id,
            user_id_to_search=user_id_to_search,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=cur_user_id)
    mock_adoption_request_repo.list_by_user.assert_not_called()

async def test_get_requests_by_user_id_use_case_user_not_found_error(
    ):
    cur_user_id: str = str(uuid4())
    user_id_to_search: str = str(uuid4())
    available_roles: list[str] = ['admin']

    mock_user_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    mock_adoption_request_repo: MagicMock = MagicMock(spec=AdoptionRequestBaseRepository)

    mock_user_repo.get_by_id.return_value = None

    use_case: GetRequestsByUserIdUseCase = GetRequestsByUserIdUseCase(
        user_repo=mock_user_repo,
        adoption_requests_repo=mock_adoption_request_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: list[AdoptionRequest] = await use_case.execute(
            cur_user_id=cur_user_id,
            user_id_to_search=user_id_to_search,
        )
    mock_user_repo.get_by_id.assert_called_once_with(id=cur_user_id)
    mock_adoption_request_repo.list_by_user.assert_not_called()
