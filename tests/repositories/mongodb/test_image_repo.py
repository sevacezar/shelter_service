
from datetime import datetime, timezone
from bson import ObjectId

from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase
import pytest

from domain.animals import Image
from repositories.mongodb.images_repo import AnimalImageMongoRepository


@pytest.fixture(scope='function')
def docs_ids() -> list[dict]:
    return [
        {'animal_id': ObjectId(), 'images_ids': [ObjectId() for _ in range(2)]},
        {'animal_id': ObjectId(), 'images_ids': [ObjectId()]},
    ]

@pytest.fixture(scope='function')
def images_dict_list(docs_ids: list[dict]) -> list[dict]:
    images: list[dict] = [
        {
            'animal_id': str(docs_ids[0].get('animal_id')),
            'filename': 'funny1.png',
            'relative_path': f'/imgs/{str(docs_ids[0].get('animal_id'))}/{str(docs_ids[0].get('images_ids')[0])}.png',
            'description': 'Funny photo # 1',
            'uploaded_at': datetime.now(timezone.utc),
            'is_avatar': True,
        },
        {
            'animal_id': str(docs_ids[0].get('animal_id')),
            'filename': 'funny2.png',
            'relative_path': f'/imgs/{str(docs_ids[0].get('animal_id'))}/{str(docs_ids[0].get('images_ids')[1])}.png',
            'description': 'Funny photo # 2',
            'uploaded_at': datetime.now(timezone.utc),
            'is_avatar': False,
        },
        {
            'animal_id': str(docs_ids[1].get('animal_id')),
            'filename': 'beautiful.png',
            'relative_path': f'/imgs/{str(docs_ids[1].get('animal_id'))}/{str(docs_ids[1].get('images_ids')[0])}.png',
            'description': 'Beautifull photo',
            'uploaded_at': datetime.now(timezone.utc),
            'is_avatar': True,
        },
    ]
    return images

@pytest.fixture(scope='function')
async def image_mongo_repo(images_dict_list: list[dict]) -> AnimalImageMongoRepository:
    mock_client: AsyncMongoMockClient = AsyncMongoMockClient()
    db: AsyncMongoMockDatabase = mock_client['test_db']

    await db['images'].insert_many((i_image for i_image in images_dict_list))
    return AnimalImageMongoRepository(db=db)