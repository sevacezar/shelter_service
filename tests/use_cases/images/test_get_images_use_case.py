from unittest.mock import MagicMock
from uuid import uuid4

from domain.animals import Image
from repositories.base.image_base_repo import BaseAnimalImageRepository
from use_cases.images.get_images import GetImagesByAnimalIdUseCase


async def test_get_images_use_case_success():
    animal_id: str = str(uuid4())

    images: list[Image] = [
        Image(
            animal_id=animal_id,
            filename='1.png',
            relative_path=f'imgs/{animal_id}/1.png',
            description='Funny photo',
            is_avatar=True,
            id=str(uuid4()),
        ),
        Image(
            animal_id=animal_id,
            filename='2.png',
            relative_path=f'imgs/{animal_id}/2.png',
            description='Funny photo 2',
            is_avatar=False,
            id=str(uuid4()),
        ),
    ]

    image_mock_repo: MagicMock = MagicMock(spec=BaseAnimalImageRepository)

    image_mock_repo.get_by_animal_id.return_value = images

    use_case: GetImagesByAnimalIdUseCase = GetImagesByAnimalIdUseCase(
        image_repo=image_mock_repo,
    )

    res: None = await use_case.execute(
        animal_id=animal_id,
    )
    assert res == images
    image_mock_repo.get_by_animal_id.assert_called_once_with(animal_id=animal_id)
