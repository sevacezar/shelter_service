# from unittest.mock import AsyncMock, patch

# from repositories.file_system.image_storage import ImageFsStorage


# class TestImageFsStorage:
#     @patch('repositories.file_system.image_storage.os.path.abspath', return_value='/mocked/animals_photos/123')
#     @patch('repositories.file_system.image_storage.os.makedirs')
#     @patch('repositories.file_system.image_storage.ImageFsStorage._get_unique_filename', return_value='/mocked/animals_photos/123/photo.png')
#     @patch('repositories.file_system.image_storage.async_open')
#     async def test_save(
#         self,
#         mock_async_open,
#         mock_get_unique_filename,
#         mock_makedirs,
#         mock_abspath,
#     ):
#         storage = ImageFsStorage(images_dir_path='/mocked/animals_photos')

#         file_content: bytes = b'Test content'
#         filename: str = 'photo.png'
#         animal_id: str = '123'

#         mock_file: AsyncMock = AsyncMock()
#         mock_async_open.return_value.__aenter__.return_value = mock_file

#         res = await storage.save(
#             file_content=file_content,
#             filename=filename,
#             animal_id=animal_id,
#         )

#         print(mock_abspath.call_args_list)
#         mock_abspath.assert_called_once_with(f'/mocked/animals_photos/123')
#         mock_makedirs.assert_any_call(f'/mocked/animals_photos', exist_ok=True)
#         mock_makedirs.assert_any_call(f'/mocked/animals_photos/{animal_id}', exist_ok=True)
#         assert mock_makedirs.call_count == 2
#         mock_get_unique_filename.assert_called_once_with(
#             directory=f'/mocked/animals_photos/{animal_id}',
#             filename=filename,
#         )
#         mock_async_open.assert_called_once_with(f'/mocked/animals_photos/{animal_id}/{filename}', 'wb')
#         mock_file.write.assert_called_once_with(file_content)
#         assert res == f'{animal_id}/{filename}'
