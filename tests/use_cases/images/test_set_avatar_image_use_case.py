from dataclasses import replace
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from domain.animals import Image
from domain.users import User
from repositories.base.image_base_repo import BaseAnimalImageRepository
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import ImageNotFound
from use_cases.images.set_avatar_image import SetAvatarImageUseCase


async def test_set_avatar_image_use_case_success(admin: User, image: Image):
    user_id: str = admin.id
    image_id: str = image.id

    available_roles: list = ['admin']

    updated_image: Image = replace(image, is_avatar=True)

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)

    user_mock_repo.get_by_id.return_value = admin
    image_mock_repo.get_by_id.return_value = image
    image_mock_repo.set_avatar.return_value = updated_image

    use_case: SetAvatarImageUseCase = SetAvatarImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        available_roles=available_roles,
    )

    res: Image = await use_case.execute(
        user_id=user_id,
        image_id=image_id,
    )
    assert res == updated_image
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_repo.get_by_id.assert_called_once_with(id=image_id)
    image_mock_repo.set_avatar.assert_called_once_with(image=image)

async def test_set_avatar_image_use_case_user_not_admin(not_admin_user: User, image: Image):
    user_id: str = not_admin_user.id
    image_id: str = image.id

    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)

    user_mock_repo.get_by_id.return_value = not_admin_user

    use_case: SetAvatarImageUseCase = SetAvatarImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: Image = await use_case.execute(
            user_id=user_id,
            image_id=image_id,
        )
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_repo.get_by_id.assert_not_called()
    image_mock_repo.set_avatar.assert_not_called()

async def test_set_avatar_image_use_case_user_not_found(image: Image):
    user_id: str = str(uuid4())
    image_id: str = image.id

    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)

    user_mock_repo.get_by_id.return_value = None

    use_case: SetAvatarImageUseCase = SetAvatarImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        available_roles=available_roles,
    )
    with pytest.raises(PermissionError):
        res: Image = await use_case.execute(
            user_id=user_id,
            image_id=image_id,
        )
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_repo.get_by_id.assert_not_called()
    image_mock_repo.set_avatar.assert_not_called()

async def test_set_avatar_image_use_case_image_not_found(admin: User):
    user_id: str = admin.id
    image_id: str = str(uuid4())

    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)

    user_mock_repo.get_by_id.return_value = admin
    image_mock_repo.get_by_id.return_value = None

    use_case: SetAvatarImageUseCase = SetAvatarImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        available_roles=available_roles,
    )

    with pytest.raises(ImageNotFound):
        res: Image = await use_case.execute(
            user_id=user_id,
            image_id=image_id,
        )
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_repo.get_by_id.assert_called_once_with(id=image_id)
    image_mock_repo.set_avatar.assert_not_called()