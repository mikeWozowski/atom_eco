from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Organization


class OrganizationRepository:
    def __init__(
            self,
            db: AsyncSession
    ) -> None:
        self.db = db

    async def get_all_organizations(self):
        result = await self.db.execute(select(Organization))
        return result.scalars().all()

    async def create_organization(self) -> Organization:
        ...