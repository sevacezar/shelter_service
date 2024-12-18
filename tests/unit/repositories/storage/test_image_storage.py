import os
from bson import ObjectId
import pytest
import shutil

from aiofile import async_open

from config import UPLOAD_DIR_PATH
from repositories.file_system.image_storage import ImageFsStorage


@pytest.fixture(scope='class', autouse=True)
def teardown():
    yield
    shutil.rmtree(UPLOAD_DIR_PATH)


@pytest.fixture(scope='function')
def image_storage() -> ImageFsStorage:
    images_dir_path: str = os.path.abspath(os.path.join(UPLOAD_DIR_PATH, 'animals_photos'))
    return ImageFsStorage(images_dir_path=images_dir_path)


class TestImageStorage:
    test_data_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))

    async def test_save_image(self, image_storage: ImageFsStorage):
        test_filename: str = 'funny_photo.png'
        test_filepath: str = os.path.join(self.test_data_path, test_filename)
        assert os.path.exists(test_filepath)

        animal_id=str(ObjectId())
        async with async_open(test_filepath, 'rb') as input_file:
            file_content: bytes = await input_file.read()
            relative_image_path: str = await image_storage.save(
                file_content=file_content,
                filename=test_filename,
                animal_id=animal_id,
            )
        saved_file_path: str = os.path.abspath(os.path.join(
            image_storage.image_dir_path,
            animal_id,
            test_filename,
        ))

        assert os.path.exists(saved_file_path)
        assert relative_image_path.split(os.sep) == [animal_id, test_filename]

        async with async_open(saved_file_path, 'rb') as file:
            saved_content: bytes = await file.read()
            assert saved_content == file_content