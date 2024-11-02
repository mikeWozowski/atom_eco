from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.fullness import FullnessRepository
from src.schemas.organization import OrganizationCreateDTO, OrganizationRetrieveDTO
from src.repositories.organization import OrganizationRepository
from src.services.organization import OrganizationService
from src.database import get_db


router = APIRouter(prefix="/api/v1/organizations")

@router.get('', response_model=list[OrganizationRetrieveDTO])
async def get_organizations(db: AsyncSession = Depends(get_db)) -> list[OrganizationRetrieveDTO]:
    organization_repository = OrganizationRepository(db)
    organization_service = OrganizationService(organization_repository)
    return await organization_service.get_organizations()


@router.post('', response_model=OrganizationRetrieveDTO)
async def create_organization(
        organization_create_dto: OrganizationCreateDTO,
        db: AsyncSession = Depends(get_db)
) -> OrganizationRetrieveDTO:
    organization_repository = OrganizationRepository(db)
    fullness_repository = FullnessRepository(db)
    organization_service = OrganizationService(organization_repository, fullness_repository)
    return await organization_service.create_organization(

    )
