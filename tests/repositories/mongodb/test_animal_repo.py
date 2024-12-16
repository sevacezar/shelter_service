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
            'birth_date': datetime(2020, 10, 1),
            'in_shelter_at': datetime(2021, 10, 1),
            'description': 'Funny dog',
            'size': 'small',
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
        },
        {
            'name': 'Rex',
            'color': 'black',
            'birth_date': datetime(2021, 10, 1),
            'in_shelter_at': datetime(2023, 10, 1),
            'description': 'Little funny dog',
            'size': 'small',
            'breed': 'breedless',
            'coat': 'medium',
            'type': 'dog',
            'gender': 'male',
            'status': 'available',
            'ok_with_children': True,
            'ok_with_cats': False,
            'ok_with_dogs': True,
            'has_vaccinations': True,
            'is_sterilized': True,
        }
    ]
    return animals

@pytest.fixture(scope='function')
async def animal_mongo_repo(animals_dict_list: list[dict]) -> AnimalMongoRepository:
    mock_client: AsyncMongoMockClient = AsyncMongoMockClient()
    db: AsyncMongoMockDatabase = mock_client['test_db']

    await db['animals'].insert_many((i_animal for i_animal in animals_dict_list))
    return AnimalMongoRepository(db=db)

class TestCreateAnimal:
    async def test_create_animal(self, animal_mongo_repo: AnimalMongoRepository):
        name = 'Jessi'
        color = 'black'
        birth_date = datetime(2021, 5, 1)
        in_shelter_at = datetime(2023, 5, 1)
        description = 'Little funny dog'
        size = 'large'
        breed = 'breedless'
        coat = 'medium'
        type = 'dog'
        gender = 'male'
        status = 'available'
        ok_with_children = True
        ok_with_cats = False
        ok_with_dogs = True
        has_vaccinations = True
        is_sterilized = True
        animal: Animal = Animal(
            name=name,
            color=color,
            birth_date=birth_date,
            in_shelter_at=in_shelter_at,
            description=description,
            size=size,
            breed=breed,
            coat=coat,
            type=type,
            gender=gender,
            status=status,
            ok_with_children=ok_with_children,
            ok_with_cats=ok_with_cats,
            ok_with_dogs=ok_with_dogs,
            has_vaccinations=has_vaccinations,
            is_sterilized=is_sterilized,
        )
        start_records_count: int = await animal_mongo_repo.collection.count_documents({})

        created_animal: Animal = await animal_mongo_repo.create(animal=animal)
        assert created_animal.id is not None
        
        cur_records_count: int = await animal_mongo_repo.collection.count_documents({})
        assert cur_records_count == start_records_count + 1

        stored_animal: dict = await animal_mongo_repo.collection.find_one({'_id': ObjectId(created_animal.id)})
        assert stored_animal is not None
        assert stored_animal.get('name') == name
        assert stored_animal.get('color') == color
        assert stored_animal.get('birth_date') == birth_date
        assert stored_animal.get('in_shelter_at') == in_shelter_at
        assert stored_animal.get('description') == description
        assert stored_animal.get('breed') == breed
        assert stored_animal.get('coat') == coat
        assert stored_animal.get('type') == type
        assert stored_animal.get('gender') == gender
        assert stored_animal.get('status') == status
        assert stored_animal.get('ok_with_children') == ok_with_children
        assert stored_animal.get('ok_with_cats') == ok_with_cats
        assert stored_animal.get('ok_with_dogs') == ok_with_dogs
        assert stored_animal.get('has_vaccinations') == has_vaccinations
        assert stored_animal.get('is_sterilized') == is_sterilized


class TestGetById:
    async def test_get_by_id_success(self, animal_mongo_repo: AnimalMongoRepository):
        new_animal: dict = {
            'name': 'Archi',
            'color': 'red',
            'birth_date': datetime(2018, 11, 1),
            "in_shelter_at": datetime(2019, 2, 1),
            'description': 'Beautifull dog',
        }
        res = await animal_mongo_repo.collection.insert_one(new_animal)
        animal_id: str = str(res.inserted_id)
        searched_animal: Animal = await animal_mongo_repo.get_by_id(id=animal_id)
        assert searched_animal
        assert searched_animal.id == animal_id

    async def test_get_by_id_not_found(self, animal_mongo_repo: AnimalMongoRepository):
        animal_id: str = str(ObjectId())
        searched_animal: Animal = await animal_mongo_repo.get_by_id(id=animal_id)
        assert searched_animal is None


class TestUpdateAnimal:
    async def test_update_success(self, animal_mongo_repo: AnimalMongoRepository):
        new_animal: dict = {
            'name': 'Archi',
            'color': 'red',
            'birth_date': datetime(2018, 11, 1),
            "in_shelter_at": datetime(2019, 2, 1),
            'description': 'Beautifull dog',
        }
        res = await animal_mongo_repo.collection.insert_one(new_animal)
        animal_id: str = str(res.inserted_id)
        animal_to_update: Animal = await animal_mongo_repo.get_by_id(id=animal_id)
        updated_params: dict = {
            'name': 'archi',
            'color': 'yellow',
            'description': 'NEW',
        }
        updated_animal: Animal = await animal_mongo_repo.update(
            animal=animal_to_update,
            updated_params=updated_params,
        )

        assert id(updated_animal) == id(animal_to_update)
        assert updated_animal.id == animal_id
        assert updated_animal.name == updated_params.get('name')
        assert updated_animal.color == updated_params.get('color')
        assert updated_animal.description == updated_params.get('description')


class TestDeleteAnimal:
    async def test_delete_success(self, animal_mongo_repo: AnimalMongoRepository):
        new_animal: dict = {
                    'name': 'Archi',
                    'color': 'red',
                    'birth_date': datetime(2018, 11, 1),
                    "in_shelter_at": datetime(2019, 2, 1),
                    'description': 'Beautifull dog',
                }
        res = await animal_mongo_repo.collection.insert_one(new_animal)
        animal_id: str = str(res.inserted_id)
        animal_to_delete: Animal = await animal_mongo_repo.get_by_id(id=animal_id)

        start_records_count: int = await animal_mongo_repo.collection.count_documents({})

        await animal_mongo_repo.delete(animal=animal_to_delete)

        cur_records_count: int = await animal_mongo_repo.collection.count_documents({})
        assert start_records_count - cur_records_count == 1
        animal: None = await animal_mongo_repo.get_by_id(id=animal_id)
        assert animal is None