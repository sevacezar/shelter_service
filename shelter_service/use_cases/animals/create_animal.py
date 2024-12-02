from datetime import datetime

from domain.animals import Animal, CoatType, AnimalGender, AnimalType, Status
from domain.users import UserRole, User
from repositories.base.animal_base_repo import AnimalBaseRepository
from repositories.base.user_base_repo import UserBaseRepository

class CreateAnimalUseCase:
    def __init__(
            self,
            animal_repo: AnimalBaseRepository,
            user_repo: UserBaseRepository,
            available_roles: list[UserRole]
        ):
        self.animal_repo = animal_repo
        self.user_repo = user_repo
        self.available_roles = available_roles

    async def execute(
            self,
            user_id: str,
            name: str,
            color: str,
            weight: int,
            birth_date: datetime,
            in_shelter_at: datetime,
            description: str,
            breed: str = 'breedless',
            coat: CoatType = CoatType.MEDIUM.value,
            type: AnimalType = AnimalType.DOG.value,
            gender: AnimalGender = AnimalGender.MALE.value,
            status: Status = Status.AVAILABLE.value,
            ok_with_children: bool = True,
            ok_with_cats: bool = True,
            ok_with_dogs: bool = True,
            has_vaccinations: bool = True,
            is_sterilized: bool = True,
    ) -> Animal:
        user: User = await self.user_repo.get_by_id(id=user_id)
        if not user or not user.role in self.available_roles:
            raise PermissionError('Create animal is forbidden')

        animal = Animal(
            name=name,
            color=color,
            weight=weight,
            birth_date=birth_date,
            in_shelter_at=in_shelter_at,
            description=description,
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
        return await self.animal_repo.create(animal=animal)
