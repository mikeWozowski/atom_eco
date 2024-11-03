from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.schemas.storage import StorageIdDTO, StorageCreateDTO
from src.models import Storage, Fullness


class StorageRepository:
    def __init__(
            self,
            db: AsyncSession
    ) -> None:
        self.db = db

    async def get_all_storages(self):
        query = (
            select(Storage)
            .options(
                joinedload(Storage.fullness).joinedload(Fullness.waste_type)
            )
        )

        result = await self.db.execute(query)
        return result.unique().scalars().all()

    async def get_storage_by_id(self, storage_id):
        query = (
            select(Storage)
            .options(
                joinedload(Storage.fullness).joinedload(Fullness.waste_type)
            )
            .where(Storage.id == storage_id)
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_storage(
            self,
            storage_create_dto: StorageCreateDTO
    ) -> StorageIdDTO:
        storage_data = storage_create_dto.model_dump(exclude_none=True)

        new_storage = Storage(**storage_data)

        self.db.add(new_storage)
        await self.db.commit()
        await self.db.refresh(new_storage)

        return StorageIdDTO.model_validate(new_storage)

    async def delete_storage_by_id(self, storage_id: int):
        storage = await self.get_storage_by_id(storage_id)
        if storage:
            await self.db.delete(storage)
            await self.db.commit()
