from typing import Any

from repositories.base.animal_base_repo import AnimalBaseRepository

class FilterAnimalsUseCase:
    def __init__(self, animal_repo: AnimalBaseRepository):
        self.animal_repo = animal_repo

    async def execute(
            self,
            filters: dict[str, Any],
            offset: int = 0,
            limit: int | None = None,
    ) -> list[Any]:
        return await self.animal_repo.get_filtered(
            filters=filters,
            offset=offset,
            limit=limit,
        )
