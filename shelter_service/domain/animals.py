from dataclasses import dataclass, asdict, field, fields
from datetime import datetime, timezone
from enum import Enum

# from domain.exceptions import MissingFileExtension


@dataclass
class Image:
    animal_id: str
    filename: str
    relative_path: str | None = None
    description: str | None = None
    id: str | None = None
    uploaded_at: datetime = datetime.now(tz=timezone.utc)
    is_avatar: bool = False

    def __bool__(self):
        return True

    @classmethod
    def from_dict(cls, image_dict: dict) -> 'Image':
        return cls(**image_dict)

    def to_dict(self):
        return asdict(self)

    # def generate_relative_path(self, prefix: str):
    #     if self.id is None:
    #         raise ValueError('id is not set. Relative path cannot be generated.')
    #     if len(self.filename.split('.')) == 1:
    #         raise MissingFileExtension('Missing image extension.')
    #     image_extension: str = self.filename.split('.')[-1]
    #     self.relative_path = prefix + str(self.id) + '.' + image_extension



class AnimalType(Enum):
    CAT: str = 'Кошка'
    DOG: str = 'Собака'


class AnimalGender(Enum):
    MALE: str = 'Мальчик'
    FEMALE: str = 'Девочка'


class CoatType(Enum):
    SHORT: str = 'Короткая'
    MEDIUM: str = 'Средняя'
    LONG: str = 'Длинная'
    HAIRLESS: str = 'Без шерсти'


class Status(Enum):
    AVAILABLE: str = 'available'
    UNAVAILABLE: str = 'unavailable'  # for example, animal in quarantine
    ADOPTED: str = 'adopted'
    RESERVED: str = 'reserved'


class Size(Enum):
    SMALL: str = 'Маленький'
    MEDIUM: str = 'Средний'
    LARGE: str = 'Большой'
    EXTRA_LARGE: str = 'Очень большой'


class Age(Enum):
    BABY: str = 'Щенок/котенок'
    JUNIOUR: str = 'Подросток'
    ADULT: str = 'Взрослый'
    SENIOR: str = 'Пожилой'

    @classmethod
    def get_age_category(cls, birth_date: datetime, datetime_now: datetime) -> str:
        years_diff: int = datetime_now.year - birth_date.year
        if (datetime_now.month, datetime_now.day) < (birth_date.month, birth_date.day):
            years_diff -= 1

        if years_diff < 1:
            return cls.BABY.value
        if years_diff < 4:
            return cls.JUNIOUR.value
        if years_diff < 8:
            return cls.ADULT.value
        return cls.SENIOR.value

        

@dataclass
class Animal:
    name: str
    color: str
    birth_date: datetime
    in_shelter_at: datetime
    description: str
    size: str = Size.MEDIUM.value
    breed: str = 'breedless'
    coat: CoatType = CoatType.MEDIUM.value
    type: AnimalType = AnimalType.DOG.value
    gender: AnimalGender = AnimalGender.MALE.value
    status: Status = Status.AVAILABLE.value
    ok_with_children: bool = True
    ok_with_cats: bool = True
    ok_with_dogs: bool = True
    has_vaccinations: bool = True
    is_sterilized: bool = True
    created_at: datetime = datetime.now(tz=timezone.utc)
    updated_at: datetime = None
    id: int | None = None
    images: list[Image] = field(default_factory=list)

    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = self.created_at

    def get_age(self, datetime_now: datetime) -> str:
        return Age.get_age_category(birth_date=self.birth_date, datetime_now=datetime_now)

    def add_images(self, images: list[Image]) -> None:
        for image in images:
            image
        self.images.extend(images)

    def remove_images(self, image_ids: list[int]) -> None:
        self.images = [image for image in self.images if image.id not in image_ids]

    def __bool__(self):
        return True

    @classmethod
    def from_dict(cls, animal_dict: dict) -> 'Animal':
        animal: 'Animal' = cls(**animal_dict)
        if animal.images:
            animal.images = [Image.from_dict(image) for image in animal.images]
        return animal

    def to_dict(self):
        return asdict(self)

    def update(self, params: dict) -> 'Animal':
        field_names: set = {field.name for field in fields(self)}
        for attr, value in params.items():
            if attr in field_names:
                self.__setattr__(attr, value)
        self.updated_at = datetime.now(tz=timezone.utc)
        return self