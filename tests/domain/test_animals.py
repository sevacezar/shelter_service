from datetime import datetime, timezone
import pytest

from domain.animals import Animal, Image
from domain.exceptions import MissingFileExtension


@pytest.fixture(scope='function')
def animal_dict() -> dict:
    creating_datetime: datetime = datetime.now(tz=timezone.utc)
    animal_dict: dict = {
        'name': 'Daisy',
        'color': 'white',
        'weight': 17,
        'birth_date': datetime(2020, 10, 1),
        'in_shelter_at': datetime(2021, 10, 1),
        'updated_at': creating_datetime,
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
        'id': 1
    }
    return animal_dict

@pytest.fixture(scope='function')
def animal(animal_dict: dict) -> Animal:
    return Animal(**animal_dict)

@pytest.fixture(scope='function')
def images() -> list[Image]:
    images_list: list[dict] = [
        {'id': 1, 'filename': 'some_image1.png', 'relative_path': 'imgs/1.png', 'description': 'some description 1', 'is_avatar': False},
        {'id': 2, 'filename': 'some_image2.png', 'relative_path': 'imgs/2.png', 'description': 'some description 2', 'is_avatar': True},
    ]
    images: list[Image] = [
        Image(**i_img_dict) for i_img_dict in images_list
    ]
    return images

def test_animal_init(animal_dict: dict):
    animal: Animal = Animal(**animal_dict)
    assert animal
    assert animal.name == animal_dict.get('name')
    assert animal.color == animal_dict.get('color')
    assert animal.weight == animal_dict.get('weight')
    assert animal.birth_date == animal_dict.get('birth_date')
    assert animal.in_shelter_at == animal_dict.get('in_shelter_at')
    assert animal.updated_at == animal_dict.get('updated_at')
    assert animal.description == animal_dict.get('description')
    assert animal.breed == animal_dict.get('breed')
    assert animal.coat == animal_dict.get('coat')
    assert animal.type == animal_dict.get('type')
    assert animal.gender == animal_dict.get('gender')
    assert animal.status == animal_dict.get('status')
    assert animal.ok_with_children == animal_dict.get('ok_with_children')
    assert animal.ok_with_cats == animal_dict.get('ok_with_cats')
    assert animal.ok_with_dogs == animal_dict.get('ok_with_dogs')
    assert animal.has_vaccinations == animal_dict.get('has_vaccinations')
    assert animal.is_sterilized == animal_dict.get('is_sterilized')
    assert animal.created_at == animal_dict.get('created_at')
    assert animal.id == animal_dict.get('id')

def test_animal_init_with_obligatory_attrs():
    animal_dict: dict = {
        'name': 'Daisy',
        'color': 'white',
        'weight': 17,
        'birth_date': datetime(2020, 10, 1),
        'in_shelter_at': datetime(2021, 10, 1),
        'description': 'Funny dog',
    }
    animal: Animal = Animal(**animal_dict)
    assert animal
    assert animal.name == animal_dict.get('name')
    assert animal.color == animal_dict.get('color')
    assert animal.weight == animal_dict.get('weight')
    assert animal.birth_date == animal_dict.get('birth_date')
    assert animal.in_shelter_at == animal_dict.get('in_shelter_at')
    assert animal.description == animal_dict.get('description')
    assert animal.breed == 'breedless'
    assert animal.coat == 'medium'
    assert animal.type == 'dog'
    assert animal.gender == 'male'
    assert animal.status == 'available'
    assert animal.ok_with_children == True
    assert animal.ok_with_cats == True
    assert animal.ok_with_dogs == True
    assert animal.has_vaccinations == True
    assert animal.is_sterilized == True
    assert animal.id == None

def test_animal_from_dict(animal_dict: dict):
    animal: Animal = Animal.from_dict(animal_dict)
    assert animal
    assert animal.name == animal_dict.get('name')
    assert animal.color == animal_dict.get('color')
    assert animal.weight == animal_dict.get('weight')
    assert animal.birth_date == animal_dict.get('birth_date')
    assert animal.in_shelter_at == animal_dict.get('in_shelter_at')
    assert animal.updated_at == animal_dict.get('updated_at')
    assert animal.description == animal_dict.get('description')
    assert animal.breed == animal_dict.get('breed')
    assert animal.coat == animal_dict.get('coat')
    assert animal.type == animal_dict.get('type')
    assert animal.gender == animal_dict.get('gender')
    assert animal.status == animal_dict.get('status')
    assert animal.ok_with_children == animal_dict.get('ok_with_children')
    assert animal.ok_with_cats == animal_dict.get('ok_with_cats')
    assert animal.ok_with_dogs == animal_dict.get('ok_with_dogs')
    assert animal.has_vaccinations == animal_dict.get('has_vaccinations')
    assert animal.is_sterilized == animal_dict.get('is_sterilized')
    assert animal.created_at == animal_dict.get('created_at')
    assert animal.id == animal_dict.get('id')

def test_animal_to_dict(animal: Animal):
    animal_dict: dict = animal.to_dict()
    assert animal_dict
    assert animal.name == animal_dict.get('name')
    assert animal.color == animal_dict.get('color')
    assert animal.weight == animal_dict.get('weight')
    assert animal.birth_date == animal_dict.get('birth_date')
    assert animal.in_shelter_at == animal_dict.get('in_shelter_at')
    assert animal.updated_at == animal_dict.get('updated_at')
    assert animal.description == animal_dict.get('description')
    assert animal.breed == animal_dict.get('breed')
    assert animal.coat == animal_dict.get('coat')
    assert animal.type == animal_dict.get('type')
    assert animal.gender == animal_dict.get('gender')
    assert animal.status == animal_dict.get('status')
    assert animal.ok_with_children == animal_dict.get('ok_with_children')
    assert animal.ok_with_cats == animal_dict.get('ok_with_cats')
    assert animal.ok_with_dogs == animal_dict.get('ok_with_dogs')
    assert animal.has_vaccinations == animal_dict.get('has_vaccinations')
    assert animal.is_sterilized == animal_dict.get('is_sterilized')
    assert animal.created_at == animal_dict.get('created_at')
    assert animal.id == animal_dict.get('id')

def test_update_animal(animal: Animal):
    start_updated_at_value: datetime = animal.updated_at
    updated_params: dict = {
        'breed': 'hasky',
        'description': 'Super dog'
    }
    updated_animal: Animal = animal.update(updated_params)
    assert updated_animal.breed == updated_params.get('breed')
    assert updated_animal.description == updated_params.get('description')
    assert updated_animal.updated_at > start_updated_at_value

def test_image_init():
    id: int = 1
    filename: str = 'some_image.png'
    ralative_path: str = 'imgs/1.png'
    descripton: str = 'Funny'
    is_avatar: bool = True
    image: Image = Image(
        filename=filename,
        id=id,
        relative_path=ralative_path,
        description=descripton,
        is_avatar=is_avatar,
    )
    assert image
    assert image.filename == filename
    assert image.id == id
    assert image.relative_path == ralative_path
    assert image.description == descripton
    assert image.is_avatar == is_avatar

def test_image_generate_path():
    id: int = 1
    filename: str = 'some_image.png'
    prefix: str = 'imgs/'
    image: Image = Image(
        id=id,
        filename=filename,
    )
    image.generate_relative_path(prefix=prefix)
    assert image
    assert image.filename == filename
    assert image.id == id
    image_extension: str = filename.split('.')[-1]
    assert image.relative_path == f'{prefix}{image.id}.{image_extension}'

def test_image_generate_path_without_extension():
    id: int = 1
    filename: str = 'some_image'
    prefix: str = 'imgs/'
    image: Image = Image(
        id=id,
        filename=filename,
    )
    with pytest.raises(MissingFileExtension):
        image.generate_relative_path(prefix=prefix)


def test_image_generate_path_without_id():
    filename: str = 'some_image.png'
    prefix: str = 'imgs/'
    image: Image = Image(filename=filename)
    with pytest.raises(ValueError):
        image.generate_relative_path(prefix=prefix)

def test_image_from_dict():
    image_dict: dict = {
        'id': 1,
        'filename': 'some_image.png',
        'relative_path': 'imgs/1.png',
        'description': 'Funny',
        'is_avatar': True,
    }
    image: Image = Image.from_dict(image_dict)
    assert image
    assert image.filename == image_dict.get('filename')
    assert image.id == image_dict.get('id')
    assert image.relative_path == image_dict.get('relative_path')
    assert image.description == image_dict.get('description')
    assert image.is_avatar == image_dict.get('is_avatar')


def test_image_to_dict():
    filename: str = 'some_image.png'
    id: int = 1
    relative_path: str = 'imgs/1.png'
    description: str = 'Funny'
    image: Image = Image(
        filename=filename,
        id=id,
        relative_path=relative_path,
        description=description,
        is_avatar=False,
    )
    image_dict: dict = image.to_dict()
    assert image_dict
    assert image.filename == image_dict.get('filename')
    assert image.id == image_dict.get('id')
    assert image.relative_path == image_dict.get('relative_path')
    assert image.description == image_dict.get('description')
    assert image.is_avatar == image_dict.get('is_avatar')

def test_animal_init_with_images(animal_dict: dict, images: list[Image]):
    animal: Animal = Animal(**animal_dict)
    animal.images = images
    assert animal
    assert animal.images
    assert animal.images[0].filename == images[0].filename
    assert animal.images[0].id == images[0].id
    assert animal.images[0].relative_path == images[0].relative_path
    assert animal.images[0].description == images[0].description

def test_animal_with_images_from_dict(animal_dict: dict):
    images_list: list[dict] = [
        {'id': 1, 'filename': 'some_image1.png', 'relative_path': 'imgs/1.png', 'description': 'some description 1'},
        {'id': 2, 'filename': 'some_image2.png', 'relative_path': 'imgs/2.png', 'description': 'some description 2'},
    ]
    animal_dict['images'] = images_list
    animal: Animal = Animal.from_dict(animal_dict)
    assert animal
    assert animal.name == animal_dict.get('name')
    assert animal.color == animal_dict.get('color')
    assert animal.weight == animal_dict.get('weight')
    assert animal.birth_date == animal_dict.get('birth_date')
    assert animal.in_shelter_at == animal_dict.get('in_shelter_at')
    assert animal.updated_at == animal_dict.get('updated_at')
    assert animal.description == animal_dict.get('description')
    assert animal.breed == animal_dict.get('breed')
    assert animal.coat == animal_dict.get('coat')
    assert animal.type == animal_dict.get('type')
    assert animal.gender == animal_dict.get('gender')
    assert animal.status == animal_dict.get('status')
    assert animal.ok_with_children == animal_dict.get('ok_with_children')
    assert animal.ok_with_cats == animal_dict.get('ok_with_cats')
    assert animal.ok_with_dogs == animal_dict.get('ok_with_dogs')
    assert animal.has_vaccinations == animal_dict.get('has_vaccinations')
    assert animal.is_sterilized == animal_dict.get('is_sterilized')
    assert animal.created_at == animal_dict.get('created_at')
    assert animal.id == animal_dict.get('id')
    assert animal.images
    assert animal.images[0].id == images_list[0].get('id')
    assert animal.images[0].filename == images_list[0].get('filename')
    assert animal.images[0].relative_path == images_list[0].get('relative_path')
    assert animal.images[0].description == images_list[0].get('description')

def test_add_images_to_animal(animal: Animal, images: list[Image]):
    assert animal.images == []
    animal.add_images(images=images)
    assert animal.images
    assert animal.images[0].filename == images[0].filename
    assert animal.images[0].id == images[0].id
    assert animal.images[0].relative_path == images[0].relative_path
    assert animal.images[0].description == images[0].description

def test_remove_images_to_animal(animal: Animal, images: list[Image]):
    animal.add_images(images=images)
    start_images_count: int = len(animal.images)
    animal.remove_images([1])
    assert len(animal.images) == start_images_count - 1
    assert animal.images[0].filename == images[1].filename
    assert animal.images[0].id == images[1].id
    assert animal.images[0].relative_path == images[1].relative_path
    assert animal.images[0].description == images[1].description

def test_animal_to_dict_with_images(animal: Animal, images: list[Image]):
    animal.add_images(images=images)
    animal_dict: dict = animal.to_dict()
    assert animal_dict

    images_list: list = animal_dict.get('images')

    assert images_list
    assert len(images_list) == len(animal.images)
    assert images_list[0].get('filename') == animal.images[0].filename
    assert images_list[0].get('id') == animal.images[0].id
    assert images_list[0].get('relative_path') == animal.images[0].relative_path
    assert images_list[0].get('description') == animal.images[0].description