from datetime import datetime, timezone
from unittest.mock import MagicMock
import pytest

from domain.animals import Animal
from repositories.base.animal_base_repo import AnimalBaseRepository
from use_cases.animals.filter_animals import FilterAnimalsUseCase

async def test_animal_filter_use_case_success():
        filters: dict = {
              'color': 'white',
              'coat': 'short',
        }
        offset: int = 1
        limit: int = 2

        filtered_animals: list[Animal] = [
              Animal(
                    name='Barsik',
                    color='white',
                    birth_date=datetime(2019, 1, 1),
                    in_shelter_at=datetime(2020, 1, 1),
                    description='Some fynny dog',
                    coat='short',
              ),
              Animal(
                    name='Tim',
                    color='white',
                    birth_date=datetime(2019, 1, 1),
                    in_shelter_at=datetime(2020, 1, 1),
                    description='Some fynny dog',
                    coat='short',
              ),
        ]

        animal_mock_repo: MagicMock = MagicMock(spec=AnimalBaseRepository)

        animal_mock_repo.get_filtered.return_value = filtered_animals

        use_case: FilterAnimalsUseCase = FilterAnimalsUseCase(
             animal_repo=animal_mock_repo,
        )
        res: Animal = await use_case.execute(
             filters=filters,
             offset=offset,
             limit=limit,
        )
        assert res == filtered_animals
        animal_mock_repo.get_filtered.assert_called_once_with(
              filters=filters,
              offset=offset,
              limit=limit,
              )
