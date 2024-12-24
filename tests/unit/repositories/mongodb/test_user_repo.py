from bson import ObjectId
from dataclasses import fields
from datetime import datetime, timezone
from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase
import pytest

from domain.users import User
from repositories.mongodb.users_repo import UserMongoRepository

@pytest.fixture(scope='function')
def users_dict_list() -> list[dict]:
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
    return users

@pytest.fixture(scope='function')
async def user_mongo_repo(users_dict_list: list[dict]) -> UserMongoRepository:
    mock_client: AsyncMongoMockClient = AsyncMongoMockClient()
    db: AsyncMongoMockDatabase = mock_client['test_db']

    for i_user in users_dict_list:
        await db['users'].insert_one(i_user)
    return UserMongoRepository(db=db)

class TestCreateUser:
    async def test_create_user(self, user_mongo_repo: UserMongoRepository):
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


class TestGetUserByEmail:
    async def test_get_by_email_success(self, user_mongo_repo: UserMongoRepository):
        email: str = 'will@smith.ru'
        user: User = await user_mongo_repo.get_by_email(email=email)
        assert user
        assert user.email == email

    async def test_get_by_email_not_found(self, user_mongo_repo: UserMongoRepository):
        email: str = 'no-found@smith.ru'
        user: User = await user_mongo_repo.get_by_email(email=email)
        assert user is None


class TestGetUserById:
    async def test_get_by_id_success(self, user_mongo_repo: UserMongoRepository):
        new_user: dict = {
            'first_name': 'Alan',
            'second_name': 'North',
            'email': 'alan@smith.ru',
            'phone': '+79129999922',
            'hashed_password': 'hashed_password',
            'role': 'user',
            'created_at': datetime.now(timezone.utc),
        }
        res = await user_mongo_repo.collection.insert_one(new_user)
        user_id: str = str(res.inserted_id)
        user: User = await user_mongo_repo.get_by_id(id=user_id)
        assert user
        assert user.id == user_id

    async def test_get_by_id_not_found(self, user_mongo_repo: UserMongoRepository):
        user_id: str = str(ObjectId())
        user: None = await user_mongo_repo.get_by_id(id=user_id)
        assert user is None


class TestUpdateUser:
    async def test_update_success(self, user_mongo_repo: UserMongoRepository):
        user: User = await user_mongo_repo.get_by_email(email='will@smith.ru')
        updated_params: dict = {
            'first_name': 'Willyam',
            'second_name': 'Smithius',
            'email': 'william@smith.ru',
            'phone': '+79129999900',
            'hashed_password': 'hashed_passwordXXXXX',
            'role': 'admin',
        }
        updated_user: User = await user_mongo_repo.update(
            user=user,
            updated_params=updated_params,
        )

        assert id(updated_user) == id(user)
        assert updated_user.id == user.id
        assert updated_user.first_name == updated_params.get('first_name')
        assert updated_user.second_name == updated_params.get('second_name')
        assert updated_user.email == updated_params.get('email')
        assert updated_user.phone == updated_params.get('phone')
        assert updated_user.hashed_password == updated_params.get('hashed_password')
        assert updated_user.role == updated_params.get('role')

    async def test_update_forbidden_params(self, user_mongo_repo: UserMongoRepository):
        user: User = await user_mongo_repo.get_by_email(email='will@smith.ru')
        updated_params: dict = {
            'id': str(ObjectId()),
            'created_at': datetime.now(timezone.utc),
        }
        updated_user: User = await user_mongo_repo.update(
            user=user,
            updated_params=updated_params,
        )

        assert id(updated_user) == id(user)
        assert updated_user.id == user.id
        assert updated_user.created_at == user.created_at


class TestDeleteUser:
    async def test_delete_success(self, user_mongo_repo: UserMongoRepository):
        user: User = await user_mongo_repo.get_by_email(email='will@smith.ru')
        start_records_count: int = await user_mongo_repo.collection.count_documents({})
        await user_mongo_repo.delete(user=user)
        cur_records_count: int = await user_mongo_repo.collection.count_documents({})

        assert start_records_count - cur_records_count == 1

        user: None = await user_mongo_repo.get_by_email(email='will@smith.ru')
        assert user is None


class TestGetAllUsers:
    async def test_get_all_users_success(
            self,
            user_mongo_repo: UserMongoRepository,
            users_dict_list: list[dict],
        ):
        cur_records_count: int = await user_mongo_repo.collection.count_documents({})
        users: list[User] = await user_mongo_repo.get_all()
        assert cur_records_count == len(users)
        user: User = users[0]
        assert isinstance(user, User)
        assert user.first_name == users_dict_list[0].get('first_name')
        assert user.second_name == users_dict_list[0].get('second_name')
        assert user.email == users_dict_list[0].get('email')
        assert user.phone == users_dict_list[0].get('phone')
        assert user.hashed_password == users_dict_list[0].get('hashed_password')
        assert user.role == users_dict_list[0].get('role')

    async def test_get_all_users_offset_success(
            self,
            user_mongo_repo: UserMongoRepository,
            users_dict_list: list[dict],
        ):
        cur_records_count: int = await user_mongo_repo.collection.count_documents({})
        offset: int = 1
        users: list[User] = await user_mongo_repo.get_all(offset=offset)
        assert len(users) == cur_records_count - offset
        user: User = users[0]
        assert isinstance(user, User)
        assert user.first_name == users_dict_list[1].get('first_name')
        assert user.second_name == users_dict_list[1].get('second_name')
        assert user.email == users_dict_list[1].get('email')
        assert user.phone == users_dict_list[1].get('phone')
        assert user.hashed_password == users_dict_list[1].get('hashed_password')
        assert user.role == users_dict_list[1].get('role')

    async def test_get_all_users_limit_success(
            self,
            user_mongo_repo: UserMongoRepository,
            users_dict_list: list[dict],
        ):
        cur_records_count: int = await user_mongo_repo.collection.count_documents({})
        limit: int = 1
        users: list[User] = await user_mongo_repo.get_all(limit=limit)
        assert len(users) == limit
        user: User = users[0]
        assert isinstance(user, User)
        assert user.first_name == users_dict_list[0].get('first_name')
        assert user.second_name == users_dict_list[0].get('second_name')
        assert user.email == users_dict_list[0].get('email')
        assert user.phone == users_dict_list[0].get('phone')
        assert user.hashed_password == users_dict_list[0].get('hashed_password')
        assert user.role == users_dict_list[0].get('role')

    async def test_get_all_users_offset_limit_success(
            self,
            user_mongo_repo: UserMongoRepository,
            users_dict_list: list[dict],
        ):
        cur_records_count: int = await user_mongo_repo.collection.count_documents({})
        offset: int = 1
        limit: int = 1
        users: list[User] = await user_mongo_repo.get_all(offset=offset, limit=limit)
        assert len(users) == limit
        user: User = users[0]
        assert isinstance(user, User)
        assert user.first_name == users_dict_list[1].get('first_name')
        assert user.second_name == users_dict_list[1].get('second_name')
        assert user.email == users_dict_list[1].get('email')
        assert user.phone == users_dict_list[1].get('phone')
        assert user.hashed_password == users_dict_list[1].get('hashed_password')
        assert user.role == users_dict_list[1].get('role')

    async def test_get_all_users_big_offset_not_found(
            self,
            user_mongo_repo: UserMongoRepository,
        ):
        offset: int = 20
        users: list[User] = await user_mongo_repo.get_all(offset=offset)
        assert len(users) == 0
