from bson import ObjectId
from datetime import datetime, timezone
from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase
import pytest

from domain.users import User
from repositories.mongodb.users_repo import UserMongoRepository

@pytest.fixture(scope='function')
async def user_mongo_repo() -> UserMongoRepository:
    mock_client: AsyncMongoMockClient = AsyncMongoMockClient()
    db: AsyncMongoMockDatabase = mock_client['test_db']

    users: list[dict] = [
        {
            'first_name': 'Steve',
            'second_name': 'Jobs',
            'email': 'steve@mail.ru',
            'phone': '+79129999999',
            'hashed_password': 'hashed_password',
            'role': 'admin',
            'created_at': datetime.now(timezone.utc),
        },
        {
            'first_name': 'Will',
            'second_name': 'Smith',
            'email': 'will@smith.ru',
            'phone': '+79129999991',
            'hashed_password': 'hashed_password',
            'role': 'user',
            'created_at': datetime.now(timezone.utc),
        }
    ]
    for i_user in users:
        await db['users'].insert_one(i_user)
    return UserMongoRepository(db=db)


async def test_create_user(user_mongo_repo: UserMongoRepository):
    first_name='Testname'
    second_name='Testov'
    email='test@mail.ru'
    phone='+12341232323'
    hashed_password='hashed'
    user: User = User(
        first_name=first_name,
        second_name=second_name,
        email=email,
        phone=phone,
        hashed_password=hashed_password,
    )
    start_records_count: int = await user_mongo_repo.collection.count_documents({})

    created_user: User = await user_mongo_repo.create(user=user)
    assert created_user.id is not None
    
    cur_records_count: int = await user_mongo_repo.collection.count_documents({})
    assert cur_records_count == start_records_count + 1

    stored_user: dict = await user_mongo_repo.collection.find_one({'_id': ObjectId(created_user.id)})
    assert stored_user is not None
    assert str(stored_user.get('_id')) == created_user.id
    assert stored_user.get('first_name') == first_name
    assert stored_user.get('second_name') == second_name
    assert stored_user.get('email') == email
    assert stored_user.get('phone') == phone
    assert stored_user.get('hashed_password') == hashed_password
    assert stored_user.get('role') == 'user'
