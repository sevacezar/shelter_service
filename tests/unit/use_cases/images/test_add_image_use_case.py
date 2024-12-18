from dataclasses import replace
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from domain.animals import Image
from domain.users import User
from repositories.base.image_base_repo import BaseAnimalImageRepository
from repositories.base.image_base_storage import BaseStorageService
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.images.add_image import AddImageUseCase


async def test_add_image_use_case_success(admin: User):
    user_id: str = admin.id
    animal_id: str = str(uuid4())
    file_content: bytes = b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
    filename: str = 'somephoto.png'
    description: str = 'funny photo'
    is_avatar: bool = True

    available_roles: list = ['admin']

    filepath: str = f'imgs/{animal_id}/somephoto.png'

    image_to_create: Image = Image(
        animal_id=animal_id,
        filename=filename,
        relative_path=filepath,
        description=description,
        is_avatar=is_avatar,
    )

    created_image: Image = replace(image_to_create, id=str(uuid4()))

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)
    image_mock_storage: MagicMock = MagicMock(spec=BaseStorageService)

    user_mock_repo.get_by_id.return_value = admin
    image_mock_storage.save.return_value = filepath
    image_mock_repo.create.return_value = created_image

    use_case: AddImageUseCase = AddImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        storage_service=image_mock_storage,
        available_roles=available_roles,
    )

    res: Image = await use_case.execute(
        user_id=user_id,
        animal_id=animal_id,
        file_content=file_content,
        filename=filename,
        description=description,
        is_avatar=is_avatar,
    )
    assert res == created_image
    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_storage.save.assert_called_once_with(
        file_content=file_content,
        filename=filename,
        animal_id=animal_id,
    )
    image_mock_repo.create.assert_called_once_with(image=image_to_create)

async def test_add_image_use_case_user_not_found():
    user_id: str = str(uuid4())
    animal_id: str = str(uuid4())
    file_content: bytes = b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
    filename: str = 'somephoto.png'
    description: str = 'funny photo'
    is_avatar: bool = True

    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)
    image_mock_storage: MagicMock = MagicMock(spec=BaseStorageService)

    user_mock_repo.get_by_id.return_value = None

    use_case: AddImageUseCase = AddImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        storage_service=image_mock_storage,
        available_roles=available_roles,
    )

    with pytest.raises(PermissionError):
        res: Image = await use_case.execute(
            user_id=user_id,
            animal_id=animal_id,
            file_content=file_content,
            filename=filename,
            description=description,
            is_avatar=is_avatar,
        )

    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_storage.save.assert_not_called()
    image_mock_repo.create.assert_not_called()

async def test_add_image_use_case_user_not_admin(not_admin_user: User):
    user_id: str = str(not_admin_user.id)
    animal_id: str = str(uuid4())
    file_content: bytes = b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
    filename: str = 'somephoto.png'
    description: str = 'funny photo'
    is_avatar: bool = True

    available_roles: list = ['admin']

    user_mock_repo: MagicMock = MagicMock(spec=UserBaseRepository)
    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)
    image_mock_storage: MagicMock = MagicMock(spec=BaseStorageService)

    user_mock_repo.get_by_id.return_value = not_admin_user

    use_case: AddImageUseCase = AddImageUseCase(
        user_repo=user_mock_repo,
        image_repo=image_mock_repo,
        storage_service=image_mock_storage,
        available_roles=available_roles,
    )

    with pytest.raises(PermissionError):
        res: Image = await use_case.execute(
            user_id=user_id,
            animal_id=animal_id,
            file_content=file_content,
            filename=filename,
            description=description,
            is_avatar=is_avatar,
        )

    user_mock_repo.get_by_id.assert_called_once_with(id=user_id)
    image_mock_storage.save.assert_not_called()
    image_mock_repo.create.assert_not_called()