from datetime import datetime, timezone
from uuid import uuid4
import pytest

from domain.users import User

@pytest.fixture(scope='function')
def user_domain() -> User:
    user_dict: dict = {
        'id': uuid4(),
        'first_name': 'John',
        'second_name': 'Smith',
        'email': 'jphn@gmail.com',
        'phone': '+79129991212',
        'hashed_password': 'hashed_password',
        'role': 'user',
        'created_at': datetime.now(tz=timezone.utc)
    }
    user: User = User(**user_dict)
    return user

def test_user_init():
    user_dict: dict = {
        'id': uuid4(),
        'first_name': 'John',
        'second_name': 'Smith',
        'email': 'jphn@gmail.com',
        'phone': '+79129991212',
        'hashed_password': 'hashed_password',
        'role': 'user',
        'created_at': datetime.now(tz=timezone.utc)
    }
    user: User = User(**user_dict)
    assert user.id == user_dict.get('id')
    assert user.first_name == user_dict.get('first_name')
    assert user.second_name == user_dict.get('second_name')
    assert user.email == user_dict.get('email')
    assert user.phone == user_dict.get('phone')
    assert user.hashed_password == user_dict.get('hashed_password')
    assert user.role == user_dict.get('role')
    assert user.created_at == user_dict.get('created_at')

def test_user_init_with_obligatory_attrs():
    user_dict: dict = {
        'first_name': 'John',
        'second_name': 'Smith',
        'email': 'jphn@gmail.com',
        'phone': '+79129991212',
        'hashed_password': 'hashed_password',
    }
    user: User = User(**user_dict)
    assert user.id is None
    assert user.first_name == user_dict.get('first_name')
    assert user.second_name == user_dict.get('second_name')
    assert user.email == user_dict.get('email')
    assert user.phone == user_dict.get('phone')
    assert user.hashed_password == user_dict.get('hashed_password')
    assert user.role == 'user'
    assert isinstance(user.created_at, datetime)

def test_user_from_dict():
    user_dict: dict = {
        'id': 1,
        'first_name': 'John',
        'second_name': 'Smith',
        'email': 'jphn@gmail.com',
        'phone': '+79129991212',
        'hashed_password': 'hashed_password',
        'role': 'user',
        'created_at': datetime.now(tz=timezone.utc)
    }
    user: User = User.from_dict(user_dict)
    assert user.id == user_dict.get('id')
    assert user.first_name == user_dict.get('first_name')
    assert user.second_name == user_dict.get('second_name')
    assert user.email == user_dict.get('email')
    assert user.phone == user_dict.get('phone')
    assert user.hashed_password == user_dict.get('hashed_password')
    assert user.role == user_dict.get('role')
    assert user.created_at == user_dict.get('created_at')

def test_user_to_dict(user_domain: User):
    user_dict: dict = user_domain.to_dict()
    assert isinstance(user_dict, dict)
    assert user_domain.id == user_dict.get('id')
    assert user_domain.first_name == user_dict.get('first_name')
    assert user_domain.second_name == user_dict.get('second_name')
    assert user_domain.email == user_dict.get('email')
    assert user_domain.phone == user_dict.get('phone')
    assert user_domain.hashed_password == user_dict.get('hashed_password')
    assert user_domain.role == user_dict.get('role')
    assert user_domain.created_at == user_dict.get('created_at')

def test_user_update(user_domain: User):
    updated_params: dict = {
        'id': uuid4(),
        'first_name': 'New first name',
        'second_name': 'New second name',
        'email': 'new_email@mail.ru',
        'phone': '+99999999999',
        'hashed_password': 'new_hashed_password',
        'role': 'admin',
        'some_field': 'some_value',
    }
    updated_user: User = user_domain.update(updated_params)
    assert updated_user.id != updated_params.get('id')
    assert updated_user.first_name == updated_params.get('first_name')
    assert updated_user.second_name == updated_params.get('second_name')
    assert updated_user.email == updated_params.get('email')
    assert updated_user.phone == updated_params.get('phone')
    assert updated_user.hashed_password == updated_params.get('hashed_password')
    assert updated_user.role != updated_params.get('role')
