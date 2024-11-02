from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.fullness import FullnessCreateDTO
from src.models import Fullness


class FullnessRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_fullness(
            self,
            fullness_create_dto: FullnessCreateDTO,
            organization_id: int | None = None,
            storage_id: int | None = None
    ) -> None:
        fullness_data = fullness_create_dto.model_dump(exclude_none=True)

        new_fullness = Fullness(**fullness_data, organization_id=organization_id, storage_id=storage_id)
        self.db.add(new_fullness)
        await self.db.commit()
        await self.db.refresh(new_fullness)
