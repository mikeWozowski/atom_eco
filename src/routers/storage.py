from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db


router = APIRouter(prefix="/api/v1/storages")

@router.get('')
async def get_storages(db: AsyncSession = Depends(get_db)) -> list:
    return []


@router.get('/{storage_id}')
async def get_storage_by_id(storage_id: int, db: AsyncSession = Depends(get_db)):
    ...


@router.post('')
async def create_storage(db: AsyncSession = Depends(get_db)):
    ...


@router.delete('/{storage_id}')
async def delete_storage_by_id(storage_id: int, db: AsyncSession = Depends(get_db)):
    ...

