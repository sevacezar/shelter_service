from bson import ObjectId
from datetime import datetime, timezone

from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase
import pytest

from domain.animal_views import AnimalView
from repositories.mongodb.animal_views_repo import AnimalViewMongoRepository


@pytest.fixture(scope='function')
def views_dict_list() -> list[dict]:
    view_id_1: ObjectId = ObjectId()
    view_id_2: ObjectId = ObjectId()
    view_id_3: ObjectId = ObjectId()

    animal_id_1: ObjectId = ObjectId()
    animal_id_2: ObjectId = ObjectId()

    user_id_1: ObjectId = ObjectId()
    user_id_2: ObjectId = ObjectId()

    views: list[dict] = [
        {'animal_id': animal_id_1, 'user_id': user_id_1, '_id': view_id_1, 'viewed_at': datetime(2024, 1, 1)},
        {'animal_id': animal_id_1, 'user_id': user_id_2, '_id': view_id_2, 'viewed_at': datetime(2024, 1, 2)},
        {'animal_id': animal_id_2, 'user_id': user_id_1, '_id': view_id_3, 'viewed_at': datetime(2024, 1, 5)},
    ]
    return views

@pytest.fixture(scope='function')
async def view_mongo_repo(views_dict_list: list[dict]) -> AnimalViewMongoRepository:
    mock_client: AsyncMongoMockClient = AsyncMongoMockClient()
    db: AsyncMongoMockDatabase = mock_client['test_db']

    await db['animal_views'].insert_many((i_view for i_view in views_dict_list))
    return AnimalViewMongoRepository(db=db)


class TestCreateView:
    async def test_create_view(self, view_mongo_repo: AnimalViewMongoRepository):
        animal_id: str = str(ObjectId())
        user_id: str = str(ObjectId())

        view: AnimalView = AnimalView(
            animal_id=animal_id,
            user_id=user_id,
        )
        start_records_count: int = await view_mongo_repo.collection.count_documents({})
        created_view: AnimalView = await view_mongo_repo.create(view=view)

        assert created_view.id is not None
        cur_records_count: int = await view_mongo_repo.collection.count_documents({})
        assert cur_records_count == start_records_count + 1
        stored_view: dict = await view_mongo_repo.collection.find_one({'_id': ObjectId(created_view.id)})
        assert stored_view is not None
        assert str(stored_view.get('animal_id')) == animal_id
        assert str(stored_view.get('user_id')) == user_id


class TestGetById:
    async def test_get_by_id_success(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
        ):
        existing_view: dict = await view_mongo_repo.collection.find_one()
        view_id: str = str(existing_view.get('_id'))
        res: AnimalView = await view_mongo_repo.get_by_id(id=view_id)

        assert res
        assert res.id == view_id

    async def test_get_by_id_not_found(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
        ):
        view_id: str = str(ObjectId())
        res: None = await view_mongo_repo.get_by_id(id=view_id)

        assert res is None


class TestDelete:
    async def test_delete(self, view_mongo_repo: AnimalViewMongoRepository):
        new_view: dict = {
            'animal_id': ObjectId(),
            'user_id': ObjectId(),
            'viewed_at': datetime.now(),
        }
        res = await view_mongo_repo.collection.insert_one(document=new_view)
        view_id: str = str(res.inserted_id)
        view_to_delete: AnimalView = await view_mongo_repo.get_by_id(id=view_id)

        start_records_count: int = await view_mongo_repo.collection.count_documents({})
        await view_mongo_repo.delete(view=view_to_delete)

        cur_records_count: int = await view_mongo_repo.collection.count_documents({})
        assert start_records_count - cur_records_count == 1
        view: None = await view_mongo_repo.get_by_id(id=view_id)
        assert view is None


class TestListByAnimal:
    async def test_list_by_animal_success(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
    ):
        existing_view: dict = await view_mongo_repo.collection.find_one()
        animal_id: str = str(existing_view.get('animal_id'))
        res: list[AnimalView] = await view_mongo_repo.list_by_animal(animal_id=animal_id)
        assert res
        assert len(res) == 2
        assert isinstance(res[0], AnimalView)

    async def test_list_by_animal_not_found(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
    ):
        animal_id: str = str(ObjectId())
        res: list[AnimalView] = await view_mongo_repo.list_by_animal(animal_id=animal_id)
        assert res == []


class TestListByUser:
    async def test_list_by_user_success(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
    ):
        existing_view: dict = await view_mongo_repo.collection.find_one()
        user_id: str = str(existing_view.get('user_id'))
        res: list[AnimalView] = await view_mongo_repo.list_by_user(user_id=user_id)
        assert res
        assert len(res) == 2
        assert isinstance(res[0], AnimalView)

    async def test_list_by_user_not_found(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
    ):
        user_id: str = str(ObjectId())
        res: list[AnimalView] = await view_mongo_repo.list_by_user(user_id=user_id)
        assert res == []


class TestGetAll:
    async def test_get_all_success(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
        ):
        cur_records_count: int = await view_mongo_repo.collection.count_documents({})
        views: list[AnimalView] = await view_mongo_repo.get_all()
        assert cur_records_count == len(views)
        view: AnimalView = views[0]
        assert isinstance(view, AnimalView)

    async def test_get_all_offset_success(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
        ):
        cur_records_count: int = await view_mongo_repo.collection.count_documents({})
        offset: int = 1
        views: list[AnimalView] = await view_mongo_repo.get_all(offset=offset)
        assert len(views) == cur_records_count - offset
        view: AnimalView = views[0]
        assert isinstance(view, AnimalView)

    async def test_get_all_limit_success(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
        ):
        cur_records_count: int = await view_mongo_repo.collection.count_documents({})
        limit: int = 1
        views: list[AnimalView] = await view_mongo_repo.get_all(limit=limit)
        assert len(views) == limit
        view: AnimalView = views[0]
        assert isinstance(view, AnimalView)

    async def test_get_all_offset_limit_success(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
        ):
        cur_records_count: int = await view_mongo_repo.collection.count_documents({})
        offset: int = 1
        limit: int = 1
        views: list[AnimalView] = await view_mongo_repo.get_all(offset=offset, limit=limit)
        assert len(views) == limit
        view: AnimalView = views[0]
        assert isinstance(view, AnimalView)


    async def test_get_all_big_offset_not_found(
            self,
            view_mongo_repo: AnimalViewMongoRepository,
        ):
        offset: int = 20
        views: list[AnimalView] = await view_mongo_repo.get_all(offset=offset)
        assert len(views) == 0