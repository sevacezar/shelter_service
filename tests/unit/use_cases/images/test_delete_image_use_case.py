from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from domain.animals import Image
from domain.users import User
from repositories.base.image_base_repo import BaseAnimalImageRepository
from repositories.base.image_base_storage import BaseStorageService
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import ImageNotFound
from use_cases.images.delete_image import DeleteImageUseCase


async def test_delete_image_use_case_success(admin: User, image: Image):
    user_id: str = admin.id
    image_id: str = image.id

    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)
    image_mock_storage: MagicMock = MagicMock(spec=BaseStorageService)

    user_mock_repo.get_by_id.return_value = admin
    image_mock_repo.get_by_id.return_value = image
    image_mock_storage.delete.return_value = True
    image_mock_repo.delete.return_value = None

    use_case: DeleteImageUseCase = DeleteImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        storage_service=image_mock_storage,
        available_roles=available_roles,
    )

    res: None = await use_case.execute(
        user_id=user_id,
        image_id=image_id,
    )
    assert res is None
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_repo.get_by_id.assert_called_once_with(id=image_id)
    image_mock_storage.delete.assert_called_once_with(relative_file_path=image.relative_path)
    image_mock_repo.delete.assert_called_once_with(image=image)

async def test_delete_image_use_case_user_not_admin(not_admin_user: User, image: Image):
    user_id: str = not_admin_user.id
    image_id: str = image.id

    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)
    image_mock_storage: MagicMock = MagicMock(spec=BaseStorageService)

    user_mock_repo.get_by_id.return_value = not_admin_user

    use_case: DeleteImageUseCase = DeleteImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        storage_service=image_mock_storage,
        available_roles=available_roles,
    )

    with pytest.raises(PermissionError):
        res: None = await use_case.execute(
            user_id=user_id,
            image_id=image_id,
        )
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_repo.get_by_id.assert_not_called()
    image_mock_storage.delete.assert_not_called()
    image_mock_repo.delete.assert_not_called()

async def test_delete_image_use_case_user_not_found():
    user_id: str = str(uuid4())
    image_id: str = str(uuid4())

    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)
    image_mock_storage: MagicMock = MagicMock(spec=BaseStorageService)

    user_mock_repo.get_by_id.return_value = None

    use_case: DeleteImageUseCase = DeleteImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        storage_service=image_mock_storage,
        available_roles=available_roles,
    )

    with pytest.raises(PermissionError):
        res: None = await use_case.execute(
            user_id=user_id,
            image_id=image_id,
        )
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_repo.get_by_id.assert_not_called()
    image_mock_storage.delete.assert_not_called()
    image_mock_repo.delete.assert_not_called()

async def test_delete_image_use_case_image_not_found(admin: User):
    user_id: str = admin.id
    image_id: str = str(uuid4())

    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)
    image_mock_storage: MagicMock = MagicMock(spec=BaseStorageService)

    user_mock_repo.get_by_id.return_value = admin
    image_mock_repo.get_by_id.return_value = None

    use_case: DeleteImageUseCase = DeleteImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        storage_service=image_mock_storage,
        available_roles=available_roles,
    )

    with pytest.raises(ImageNotFound):
        res: None = await use_case.execute(
            user_id=user_id,
            image_id=image_id,
        )
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_repo.get_by_id.assert_called_once_with(id=image_id)
    image_mock_storage.delete.assert_not_called()
    image_mock_repo.delete.assert_not_called()