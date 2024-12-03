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
    CAT: str = 'cat'
    DOG: str = 'dog'


class AnimalGender(Enum):
    MALE: str = 'male'
    FEMALE: str = 'female'


class CoatType(Enum):
    SHORT: str = 'short'
    MEDIUM: str = 'medium'
    LONG: str = 'long'


class Status(Enum):
    AVAILABLE: str = 'available'
    UNAVAILAble: str = 'unavailable'  # for example, animal in quarantine
    ADOPTED: str = 'adopted'
    RESERVED: str = 'reserved'


@dataclass
class Animal:
    name: str
    color: str
    weight: int
    birth_date: datetime
    in_shelter_at: datetime
    description: str
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