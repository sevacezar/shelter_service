
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
            'relative_path': f'/imgs/{str(docs_ids[0].get("animal_id"))}/{str(docs_ids[0].get("images_ids")[0])}.png',
            'description': 'Funny photo # 1',
            'uploaded_at': datetime.now(timezone.utc),
            'is_avatar': True,
            '_id': docs_ids[0].get("images_ids")[0],
        },
        {
            'animal_id': str(docs_ids[0].get('animal_id')),
            'filename': 'funny2.png',
            'relative_path': f'/imgs/{str(docs_ids[0].get("animal_id"))}/{str(docs_ids[0].get("images_ids")[1])}.png',
            'description': 'Funny photo # 2',
            'uploaded_at': datetime.now(timezone.utc),
            'is_avatar': False,
            '_id':docs_ids[0].get("images_ids")[1],
        },
        {
            'animal_id': str(docs_ids[1].get('animal_id')),
            'filename': 'beautiful.png',
            'relative_path': f'/imgs/{str(docs_ids[1].get("animal_id"))}/{str(docs_ids[1].get("images_ids")[0])}.png',
            'description': 'Beautifull photo',
            'uploaded_at': datetime.now(timezone.utc),
            'is_avatar': True,
            '_id': docs_ids[1].get("images_ids")[0],
        },
    ]
    return images

@pytest.fixture(scope='function')
async def image_mongo_repo(images_dict_list: list[dict]) -> AnimalImageMongoRepository:
    mock_client: AsyncMongoMockClient = AsyncMongoMockClient()
    db: AsyncMongoMockDatabase = mock_client['test_db']

    await db['images'].insert_many((i_image for i_image in images_dict_list))
    return AnimalImageMongoRepository(db=db)


class TestCreate:
    async def test_create_image(
            self,
            image_mongo_repo: AnimalImageMongoRepository,
        ):
        animal_id: str = str(ObjectId())
        filename: str = 'new_photo.png'
        description: str = 'New funny photo'

        image: Image = Image(
            animal_id=animal_id,
            filename=filename,
            description=description,
        )

        start_records_count: int = await image_mongo_repo.collection.count_documents({})
        created_image: Image = await image_mongo_repo.create(image=image)

        assert created_image.id is not None
        cur_records_count: int = await image_mongo_repo.collection.count_documents({})
        assert cur_records_count == start_records_count + 1
        stored_image: dict = await image_mongo_repo.collection.find_one({'_id': ObjectId(created_image.id)})
        assert stored_image is not None
        assert stored_image.get('animal_id') == animal_id
        assert stored_image.get('filename') == filename
        assert stored_image.get('description') == description


class TestGetById:
    async def test_get_by_id_success(
            self,
            image_mongo_repo: AnimalImageMongoRepository,
        ):
        existing_image: dict = await image_mongo_repo.collection.find_one()
        image_id: str = str(existing_image.get('_id'))
        res: Image = await image_mongo_repo.get_by_id(id=image_id)

        assert res
        assert res.id == image_id

    async def test_get_by_id_not_found(
            self,
            image_mongo_repo: AnimalImageMongoRepository,
        ):
        image_id: str = str(ObjectId())
        res: None = await image_mongo_repo.get_by_id(id=image_id)

        assert res is None


class TestGetByAnimalId:
    async def test_get_by_animal_id_success(
            self,
            image_mongo_repo: AnimalImageMongoRepository,
    ):
        existing_image: dict = await image_mongo_repo.collection.find_one()
        animal_id: str = str(existing_image.get('animal_id'))
        res: list[Image] = await image_mongo_repo.get_by_animal_id(animal_id=animal_id)
        assert res
        assert len(res) == 2
        assert isinstance(res[0], Image)

    async def test_get_by_animal_id_not_found(
            self,
            image_mongo_repo: AnimalImageMongoRepository,
    ):
        animal_id: str = str(ObjectId())
        res: list[Image] = await image_mongo_repo.get_by_animal_id(animal_id=animal_id)
        assert res == []


class TestDelete:
    async def test_delete(self, image_mongo_repo: AnimalImageMongoRepository):
        new_image: dict = {
            'animal_id': str(ObjectId()),
            'filename': 'img.png',
            'description': 'some desc',
        }
        res = await image_mongo_repo.collection.insert_one(document=new_image)
        image_id: str = str(res.inserted_id)
        image_to_delete: Image = await image_mongo_repo.get_by_id(id=image_id)

        start_records_count: int = await image_mongo_repo.collection.count_documents({})
        await image_mongo_repo.delete(image=image_to_delete)

        cur_records_count: int = await image_mongo_repo.collection.count_documents({})
        assert start_records_count - cur_records_count == 1
        image: None = await image_mongo_repo.get_by_id(id=image_id)
        assert image is None


class TestSetAvatar:
    async def test_set_image_avatar(self, image_mongo_repo: AnimalImageMongoRepository):
        existing_image: dict = await image_mongo_repo.collection.find_one()
        animal_id: str = str(existing_image.get('animal_id'))
        images: list[Image] = await image_mongo_repo.get_by_animal_id(animal_id=animal_id)

        assert images[0].is_avatar == True
        assert images[-1].is_avatar == False

        image_to_setting_avatar: Image = images[-1]
        res: Image = await image_mongo_repo.set_avatar(image=image_to_setting_avatar)
        assert id(res) == id(image_to_setting_avatar)
        assert res.is_avatar == True

        images_after_setting: list[Image] = await image_mongo_repo.get_by_animal_id(animal_id=animal_id)
        assert images_after_setting[0].is_avatar == False
        assert images_after_setting[-1].is_avatar == True


class TestUpdateDescription:
    async def test_update_description(
            self,
            image_mongo_repo: AnimalImageMongoRepository,
    ):
        new_description: str = 'NEW DESCRIPTION'
        existing_image: dict = await image_mongo_repo.collection.find_one()
        image_id: str = str(existing_image.get('_id'))
        image_to_update: Image = await image_mongo_repo.get_by_id(id=image_id)
        res: Image = await image_mongo_repo.update_description(
            image=image_to_update,
            description=new_description,
        )
        assert id(res) == id(image_to_update)
        assert res.description == new_description

        stored_image = await image_mongo_repo.collection.find_one({'_id': ObjectId(image_id)})
        assert stored_image.get('description') == new_description

