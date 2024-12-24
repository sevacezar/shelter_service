from bson import ObjectId
from datetime import datetime, timedelta, timezone

from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase
import pytest

from domain.adoption_requests import AdoptionRequest
from repositories.mongodb.adoption_request_repo import AdoptionRequestMongoRepository


@pytest.fixture(scope='function')
def adoption_requests_dict_list() -> list[dict]:
    request_id_1: ObjectId = ObjectId()
    request_id_2: ObjectId = ObjectId()
    request_id_3: ObjectId = ObjectId()

    animal_id_1: ObjectId = ObjectId()
    animal_id_2: ObjectId = ObjectId()

    user_id_1: ObjectId = ObjectId()
    user_id_2: ObjectId = ObjectId()

    requests: list[dict] = [
        {
            'animal_id': animal_id_1,
            'user_id': user_id_1,
            'status': 'pending',
            'user_comment': 'I want adopt thitpretty dog!',
            'created_at': datetime(2024, 1, 1),
            'updated_at': datetime(2024, 1, 1),
            '_id': request_id_1,
        },
        {
            'animal_id': animal_id_1,
            'user_id': user_id_2,
            'status': 'cancelled',
            'user_comment': 'Some comment',
            'created_at': datetime(2023, 10, 1),
            'updated_at': datetime(2023, 10, 2),
            '_id': request_id_2,
        },
         {
            'animal_id': animal_id_2,
            'user_id': user_id_1,
            'status': 'rejected',
            'user_comment': 'Some comment',
            'created_at': datetime(2023, 12, 1),
            'updated_at': datetime(2023, 12, 2),
            '_id': request_id_3,
        },
    ]
    return requests

@pytest.fixture(scope='function')
async def adoption_request_mongo_repo(adoption_requests_dict_list: list[dict]) -> AdoptionRequestMongoRepository:
    mock_client: AsyncMongoMockClient = AsyncMongoMockClient()
    db: AsyncMongoMockDatabase = mock_client['test_db']

    await db['adoption_requests'].insert_many((i_request for i_request in adoption_requests_dict_list))
    return AdoptionRequestMongoRepository(db=db)


class TestCreate:
    async def test_create_request(self, adoption_request_mongo_repo: AdoptionRequestMongoRepository):
        animal_id: str = str(ObjectId())
        user_id: str = str(ObjectId())

        request: AdoptionRequest = AdoptionRequest(
            animal_id=animal_id,
            user_id=user_id,
            user_comment='I want',
        )
        start_records_count: int = await adoption_request_mongo_repo.collection.count_documents({})
        created_request: AdoptionRequest = await adoption_request_mongo_repo.create(request=request)

        assert created_request.id is not None
        cur_records_count: int = await adoption_request_mongo_repo.collection.count_documents({})
        assert cur_records_count == start_records_count + 1
        stored_request: dict = await adoption_request_mongo_repo.collection.find_one({'_id': ObjectId(created_request.id)})
        assert stored_request is not None
        assert str(stored_request.get('animal_id')) == animal_id
        assert str(stored_request.get('user_id')) == user_id


class TestGetById:
    async def test_get_by_id_success(
            self,
            adoption_request_mongo_repo: AdoptionRequestMongoRepository,
        ):
        existing_request: dict = await adoption_request_mongo_repo.collection.find_one()
        request_id: str = str(existing_request.get('_id'))
        res: AdoptionRequest = await adoption_request_mongo_repo.get_by_id(id=request_id)

        assert res
        assert res.id == request_id

    async def test_get_by_id_not_found(
            self,
            adoption_request_mongo_repo: AdoptionRequestMongoRepository,
        ):
        request_id: str = str(ObjectId())
        res: None = await adoption_request_mongo_repo.get_by_id(id=request_id)

        assert res is None


class TestUpdateStatus:
    async def test_update_status(self, adoption_request_mongo_repo: AdoptionRequestMongoRepository):
        start_status: str = 'pending'
        created_at: datetime = datetime.now() - timedelta(1)
        request_to_update_dict: dict = {
            'animal_id': ObjectId(),
            'user_id': ObjectId(),
            'status': start_status,
            'created_at': created_at,
            'updated_at': created_at,
        }
        res = await adoption_request_mongo_repo.collection.insert_one(request_to_update_dict)
        request_id: ObjectId = res.inserted_id
        request_to_update_obj: AdoptionRequest = await adoption_request_mongo_repo.get_by_id(id=str(request_id))
        updated_request_obj: AdoptionRequest = await adoption_request_mongo_repo.update_status(
            request=request_to_update_obj,
            new_status='approved',
        )
        assert updated_request_obj
        assert id(updated_request_obj) == id(request_to_update_obj)
        assert updated_request_obj.status == 'approved'
        stored_request: dict = await adoption_request_mongo_repo.collection.find_one({'_id': request_id})
        assert stored_request.get('status') == 'approved'
        assert stored_request.get('updated_at') > stored_request.get('created_at')


class TestDelete:
    async def test_delete(self, adoption_request_mongo_repo: AdoptionRequestMongoRepository):
        new_request: dict = {
            'animal_id': ObjectId(),
            'user_id': ObjectId(),
            'status': 'pending',
            'user_comment': 'This',
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
        }
        res = await adoption_request_mongo_repo.collection.insert_one(document=new_request)
        request_id: str = str(res.inserted_id)
        request_to_delete: AdoptionRequest = await adoption_request_mongo_repo.get_by_id(id=request_id)

        start_records_count: int = await adoption_request_mongo_repo.collection.count_documents({})
        await adoption_request_mongo_repo.delete(request=request_to_delete)

        cur_records_count: int = await adoption_request_mongo_repo.collection.count_documents({})
        assert start_records_count - cur_records_count == 1
        request: None = await adoption_request_mongo_repo.get_by_id(id=request_id)
        assert request is None
