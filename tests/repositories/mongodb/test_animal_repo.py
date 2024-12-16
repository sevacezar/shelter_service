from bson import ObjectId
from datetime import datetime, timezone

from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase
import pytest

from domain.animals import Animal
from repositories.mongodb.animals_repo import AnimalMongoRepository

@pytest.fixture(scope='function')
def animals_dict_list() -> list[dict]:
    animals: list[dict] = [
        {
            'name': 'Daisy',
            'color': 'white',
            'size': 'medium',
            'birth_date': datetime(2020, 10, 1),
            'in_shelter_at': datetime(2021, 10, 1),
            'description': 'Funny dog',
            'breed': 'breedless',
            'coat': 'medium',
            'type': 'dog',
            'gender': 'female',
            'status': 'available',
            'ok_with_children': True,
            'ok_with_cats': True,
            'ok_with_dogs': False,
            'has_vaccinations': True,
            'is_sterilized': True,
            'created_at': creating_datetime,
            'id': '1',
        }
    ]