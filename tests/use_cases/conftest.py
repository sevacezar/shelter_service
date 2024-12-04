from datetime import datetime, timezone
from uuid import uuid4
import pytest

from domain.animals import Animal, Image
from domain.users import User, UserRole

@pytest.fixture(scope='function')
def admin() -> User:
    return User(
        first_name='Poul',
        second_name='Black',
        email='admin@mail.ru',
        phone='+77777777777',
        hashed_password='hashed_password',
        role=UserRole.ADMIN.value,
        id=uuid4(),
    )

@pytest.fixture(scope='function')
def not_admin_user() -> User:
    return User(
        first_name='Poul',
        second_name='Black',
        email='not_admin@mail.ru',
        phone='+77777777777',
        hashed_password='hashed_password',
        id=uuid4(),
    )

@pytest.fixture(scope='function')
def animal() -> Animal:
    return Animal(
            name='Daysy',
            color='white',
            weight=17,
            birth_date=datetime(2020, 1, 1, tzinfo=timezone.utc),
            in_shelter_at=datetime(2021, 1, 1, tzinfo=timezone.utc),
            description='Fynny dog',
            id=uuid4(),
        )

@pytest.fixture(scope='function')
def image() -> Image:
    animal_id: str = str(uuid4())
    filename: str = 'funny.png'
    return Image(
            animal_id=animal_id,
            filename=filename,
            relative_path=f'imgs/{animal_id}/{filename}',
            description='Funny photo',
            is_avatar=False,
            id=str(uuid4()),
        )