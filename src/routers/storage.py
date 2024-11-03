from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.storage import StorageRetrieveDTO, StorageIdDTO, StorageCreateDTO
from src.schemas.fullness import FullnessCreateDTO
from src.services.storage import StorageService
from src.repositories.fullness import FullnessRepository
from src.repositories.storage import StorageRepository
from src.database import get_db


router = APIRouter(prefix="/api/v1/storages")

@router.get('', response_model=list[StorageRetrieveDTO])
async def get_storages(db: AsyncSession = Depends(get_db)) -> list[StorageRetrieveDTO]:
    storage_repository = StorageRepository(db)
    fullness_repository = FullnessRepository(db)
    storage_service = StorageService(storage_repository, fullness_repository)

    return await storage_service.get_storages()


@router.get('/{storage_id}', response_model=StorageRetrieveDTO)
async def get_storage_by_id(storage_id: int, db: AsyncSession = Depends(get_db)) -> StorageRetrieveDTO:
    storage_repository = StorageRepository(db)
    fullness_repository = FullnessRepository(db)
    storage_service = StorageService(storage_repository, fullness_repository)

    return await storage_service.get_storage_by_id(storage_id)


@router.post('')
async def create_storage(
        storage: StorageCreateDTO,
        fullness_data: list[FullnessCreateDTO],
        db: AsyncSession = Depends(get_db)
) -> StorageIdDTO:
    storage_repository = StorageRepository(db)
    fullness_repository = FullnessRepository(db)
    storage_service = StorageService(storage_repository, fullness_repository)

    return await storage_service.create_storage(storage, fullness_data)


@router.delete('/{storage_id}')
async def delete_storage_by_id(storage_id: int, db: AsyncSession = Depends(get_db)):
    storage_repository = StorageRepository(db)
    fullness_repository = FullnessRepository(db)
    storage_service = StorageService(storage_repository, fullness_repository)

    await storage_service.delete_storage_by_id(storage_id)
    return {"message": "Storage deleted successfully"}
