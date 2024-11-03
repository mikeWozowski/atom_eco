from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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

    async def get_fullness_by_organization_id(self, organization_id: int, waste_type_id: int):
        query = (
            select(Fullness)
            .options(selectinload(Fullness.waste_type))
            .where(
                Fullness.organization_id == organization_id,
                Fullness.waste_type_id == waste_type_id
            )
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_fullness(self, fullness_id: int, new_fill: int):
        query = (
            update(Fullness)
            .where(Fullness.id == fullness_id)
            .values(current_fill=new_fill)
        )
        await self.db.execute(query)
        await self.db.commit()
