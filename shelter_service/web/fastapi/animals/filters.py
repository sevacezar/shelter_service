from enum import Enum

from domain.animals import (
    AnimalType,
    AnimalGender,
    CoatType,
    Size,
    Age,
)


class FiltersManager:
    metadata: dict[Enum, dict] = {
        AnimalType: {
            'name': 'Тип животного',
            'query_param_name': 'animal_type',
            'label_name': 'Выберите тип питомца',
        },
        AnimalGender: {
            'name': 'Пол',
            'query_param_name': 'gender',
            'label_name': 'Выберите пол',
        },
        CoatType: {
            'name': 'Тип шерсти',
            'query_param_name': 'coat',
            'label_name': 'Выберите тип шерсти',
        },
        Size: {
            'name': 'Размер',
            'query_param_name': 'size',
            'label_name': 'Выберите размер',
        },
        Age: {
            'name': 'Возраст',
            'query_param_name': 'age_type',
            'label_name': 'Выберите возраст',
        },
    }

    @classmethod
    def get_filters_data_with_options(cls) -> list[dict]:
        """Get filters data"""
        filters: list = []
        for enum_class, metadata in cls.metadata.items():
            item = metadata
            item.update({'options': [option.value for option in enum_class]})
            filters.append(item)
        return filters
    