from datetime import datetime
import pytest

from domain.animal_views import AnimalView

@pytest.fixture(scope='function')
def animal_view_dict() -> dict:
    return {
        'id': '1',
        'user_id': '1',
        'animal_id': '2',
        'viewed_at': datetime(2020, 1, 1),
    }

@pytest.fixture(scope='function')
def animal_view(animal_view_dict: dict) -> AnimalView:
    return AnimalView(**animal_view_dict)

def test_init_animal_view(animal_view_dict: dict):
    animal_view_obj: AnimalView = AnimalView(**animal_view_dict)
    assert animal_view_obj
    assert animal_view_obj.id == animal_view_dict.get('id')
    assert animal_view_obj.user_id == animal_view_dict.get('user_id')
    assert animal_view_obj.animal_id == animal_view_dict.get('animal_id')
    assert animal_view_obj.viewed_at == animal_view_dict.get('viewed_at')

def test_init_animal_view_with_obligatory_attrs():
    animal_view_dict: dict = {
        'user_id': 'user_id',
        'animal_id': 'animal_id',
    }
    animal_view_obj: AnimalView = AnimalView(**animal_view_dict)
    assert animal_view_obj
    assert animal_view_obj.id == None
    assert animal_view_obj.user_id == animal_view_dict.get('user_id')
    assert animal_view_obj.animal_id == animal_view_dict.get('animal_id')
    assert animal_view_obj.viewed_at

def test_animal_view_from_dict(animal_view_dict: dict):
    animal_view_obj: AnimalView = AnimalView.from_dict(animal_view_dict)
    assert animal_view_obj
    assert animal_view_obj.id == animal_view_dict.get('id')
    assert animal_view_obj.user_id == animal_view_dict.get('user_id')
    assert animal_view_obj.animal_id == animal_view_dict.get('animal_id')
    assert animal_view_obj.viewed_at == animal_view_dict.get('viewed_at')

def test_animal_view_to_dict(animal_view: AnimalView):
    animal_view_dict: dict = animal_view.to_dict()
    assert animal_view_dict
    assert animal_view.id == animal_view_dict.get('id')
    assert animal_view.user_id == animal_view_dict.get('user_id')
    assert animal_view.animal_id == animal_view_dict.get('animal_id')
    assert animal_view.viewed_at == animal_view_dict.get('viewed_at')
