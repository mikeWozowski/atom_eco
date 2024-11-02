from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Fullness


class FullnessRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_fullness(self) -> Fullness:
        ...
