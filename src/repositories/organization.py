from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.schemas.organization import OrganizationIdDTO, OrganizationCreateDTO
from src.models import Organization, Fullness


class OrganizationRepository:
    def __init__(
            self,
            db: AsyncSession
    ) -> None:
        self.db = db

    async def get_all_organizations(self):
        query = (
            select(Organization)
            .options(
                joinedload(Organization.fullness).joinedload(Fullness.waste_type)
            )
        )

        result = await self.db.execute(query)
        return result.unique().scalars().all()

    async def get_organization_by_id(self, organization_id: int):
        query = (
            select(Organization)
            .options(
                joinedload(Organization.fullness).joinedload(Fullness.waste_type)
            )
            .where(Organization.id == organization_id)
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_organization(
            self,
            organization_create_dto: OrganizationCreateDTO
    ) -> OrganizationIdDTO:
        organization_data = organization_create_dto.model_dump(exclude_none=True)

        new_organization = Organization(**organization_data)

        self.db.add(new_organization)
        await self.db.commit()
        await self.db.refresh(new_organization)

        return OrganizationIdDTO.model_validate(new_organization)

    async def delete_organization_by_id(self, organization_id: int):
        organization = await self.get_organization_by_id(organization_id)
        if organization:
            await self.db.delete(organization)
            await self.db.commit()
