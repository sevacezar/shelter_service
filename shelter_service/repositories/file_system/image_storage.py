from aiofile import async_open
import os

from repositories.base.image_base_storage import BaseStorageService


class ImageFsStorage(BaseStorageService):
    def __init__(self, images_dir_path: str):
        os.makedirs(images_dir_path, exist_ok=True)
        self.image_dir_path = images_dir_path

    def _get_unique_filename(self, directory: str, filename: str) -> str:
        base, extension = os.path.splitext(filename)
        counter = 1

        new_filename = filename
        while os.path.exists(os.path.join(directory, new_filename)):
            new_filename = f'{base}({counter}){extension}'
            counter += 1
        return os.path.join(directory, new_filename)

    async def save(
            self,
            file_content: bytes,
            filename: str,
            animal_id: str
        ) -> str:
        animal_images_path: str = os.path.abspath(os.path.join(
            self.image_dir_path,
            animal_id,
        ))
        os.makedirs(animal_images_path, exist_ok=True)
        image_path = self._get_unique_filename(
            directory=animal_images_path,
            filename=filename,
        )

        async with async_open(image_path, 'wb') as file:
            await file.write(file_content)

        return os.path.relpath(path=image_path, start=self.image_dir_path)

    async def delete(self, relative_file_path: str) -> bool:
        file_path: str = os.path.abspath(os.path.join(self.image_dir_path, relative_file_path))
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False