from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.storage import StorageRepository
from src.services.storage import StorageService
from src.schemas.waste import FillWasteDTO
from src.schemas.fullness import FullnessCreateDTO
from src.schemas.organization import OrganizationCreateDTO, OrganizationRetrieveDTO, OrganizationIdDTO
from src.repositories.fullness import FullnessRepository
from src.repositories.organization import OrganizationRepository
from src.services.organization import OrganizationService
from src.database import get_db


router = APIRouter(prefix="/api/v1/organizations")


@router.get('', response_model=list[OrganizationRetrieveDTO])
async def get_organizations(db: AsyncSession = Depends(get_db)) -> list[OrganizationRetrieveDTO]:
    organization_repository = OrganizationRepository(db)
    fullness_repository = FullnessRepository(db)
    organization_service = OrganizationService(organization_repository, fullness_repository)

    return await organization_service.get_organizations()


@router.get('/{organization_id}', response_model=OrganizationRetrieveDTO)
async def get_organization_by_id(organization_id: int, db: AsyncSession = Depends(get_db)) -> OrganizationRetrieveDTO:
    organization_repository = OrganizationRepository(db)
    fullness_repository = FullnessRepository(db)
    organization_service = OrganizationService(organization_repository, fullness_repository)

    return await organization_service.get_organization_by_id(organization_id)


@router.post('', response_model=OrganizationIdDTO)
async def create_organization(
        organization: OrganizationCreateDTO,
        fullness_data: list[FullnessCreateDTO],
        db: AsyncSession = Depends(get_db)
) -> OrganizationIdDTO:
    organization_repository = OrganizationRepository(db)
    fullness_repository = FullnessRepository(db)
    organization_service = OrganizationService(organization_repository, fullness_repository)

    return await organization_service.create_organization(organization, fullness_data)


@router.delete('/{organization_id}', response_description="Delete an organization")
async def delete_organization_by_id(organization_id: int, db: AsyncSession = Depends(get_db)):
    organization_repository = OrganizationRepository(db)
    fullness_repository = FullnessRepository(db)
    organization_service = OrganizationService(organization_repository, fullness_repository)

    await organization_service.delete_organization_by_id(organization_id)
    return {"message": "Organization deleted successfully"}


@router.get('/{organization_id}/storages')
async def get_all_storages(organization_id: int, db: AsyncSession = Depends(get_db)):
    organization_repository = OrganizationRepository(db)
    storage_repository = StorageRepository(db)
    fullness_repository = FullnessRepository(db)
    storage_service = StorageService(storage_repository, fullness_repository, organization_repository)

    storages_info = await storage_service.get_storages_with_info(organization_id)
    return storages_info

@router.patch("/{organization_id}/fill-waste")
async def fill_waste(
        organization_id: int,
        fill_waste_dto: FillWasteDTO,
        db: AsyncSession = Depends(get_db)
):
    organization_repository = OrganizationRepository(db)
    fullness_repository = FullnessRepository(db)
    organization_service = OrganizationService(organization_repository, fullness_repository)

    result = await organization_service.fill_waste(organization_id, fill_waste_dto.waste_type_id, fill_waste_dto.amount)

    return result

@router.patch("/{organization_id}/recycle")
async def recycle(
        organization_id: int,
        db: AsyncSession = Depends(get_db)
):
    ...
