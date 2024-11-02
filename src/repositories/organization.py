from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.organization import OrganizationIdDTO, OrganizationCreateDTO, OrganizationRetrieveDTO
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

    async def get_organization_by_id(self, organization_id: int) -> OrganizationRetrieveDTO:
        result = await self.db.execute(select(Organization).where(Organization.id == organization_id))
        organization = result.scalars().first()

        return OrganizationRetrieveDTO.model_validate(organization)

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
