from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Storage


class StorageRepository:
    def __init__(
            self,
            db: AsyncSession
    ) -> None:
        self.db = db

    async def get_all_storages(self):
        result = await self.db.execute(select(Storage))
        return result.scalars().all()

    async def get_storage_by_id(self, storage_id):
        ...

    async def create_storage(self):
        ...

    async def delete_storage(self):
        ...
