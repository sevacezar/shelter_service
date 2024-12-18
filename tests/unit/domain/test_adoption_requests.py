from datetime import datetime
import pytest

from domain.adoption_requests import AdoptionRequest

@pytest.fixture(scope='function')
def adoption_request_dict() -> dict:
    created_at: datetime = datetime(2020, 1, 1)
    return {
        'id': '1',
        'user_id': '1',
        'animal_id': '2',
        'status': 'pending',
        'created_at': created_at,
        'updated_at': created_at,
    }

@pytest.fixture(scope='function')
def adoption_request(adoption_request_dict: dict) -> AdoptionRequest:
    return AdoptionRequest(**adoption_request_dict)

def test_init_adoption_request(adoption_request_dict: dict):
    adoption_request_obj: AdoptionRequest = AdoptionRequest(**adoption_request_dict)
    assert adoption_request_obj
    assert adoption_request_obj.id == adoption_request_dict.get('id')
    assert adoption_request_obj.user_id == adoption_request_dict.get('user_id')
    assert adoption_request_obj.animal_id == adoption_request_dict.get('animal_id')
    assert adoption_request_obj.status == adoption_request_dict.get('status')
    assert adoption_request_obj.created_at == adoption_request_dict.get('created_at')
    assert adoption_request_obj.updated_at == adoption_request_dict.get('updated_at')

def test_init_adoption_request_with_obligatory_attrs():
    adoption_request_dict: dict = {
        'user_id': 'user_id',
        'animal_id': 'animal_id',
        'status': 'pending',
    }
    apotion_request_obj: AdoptionRequest = AdoptionRequest(**adoption_request_dict)
    assert apotion_request_obj
    assert apotion_request_obj.id == None
    assert apotion_request_obj.user_id == adoption_request_dict.get('user_id')
    assert apotion_request_obj.animal_id == adoption_request_dict.get('animal_id')
    assert apotion_request_obj.status == adoption_request_dict.get('status')
    assert apotion_request_obj.created_at == apotion_request_obj.updated_at

def test_adoption_request_from_dict(adoption_request_dict: dict):
    adoption_request_obj: AdoptionRequest = AdoptionRequest.from_dict(adoption_request_dict)
    assert adoption_request_obj
    assert adoption_request_obj.id == adoption_request_dict.get('id')
    assert adoption_request_obj.user_id == adoption_request_dict.get('user_id')
    assert adoption_request_obj.animal_id == adoption_request_dict.get('animal_id')
    assert adoption_request_obj.status == adoption_request_dict.get('status')
    assert adoption_request_obj.created_at == adoption_request_dict.get('created_at')
    assert adoption_request_obj.updated_at == adoption_request_dict.get('updated_at')

def test_adoption_request_to_dict(adoption_request: AdoptionRequest):
    adoption_request_dict: dict = adoption_request.to_dict()
    assert adoption_request_dict
    assert adoption_request.id == adoption_request_dict.get('id')
    assert adoption_request.user_id == adoption_request_dict.get('user_id')
    assert adoption_request.animal_id == adoption_request_dict.get('animal_id')
    assert adoption_request.status == adoption_request_dict.get('status')
    assert adoption_request.created_at == adoption_request_dict.get('created_at')
    assert adoption_request.updated_at == adoption_request_dict.get('updated_at')
