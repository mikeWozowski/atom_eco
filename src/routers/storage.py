from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db


router = APIRouter(prefix="/api/v1/storages")

@router.get('')
async def get_storages(db: AsyncSession = Depends(get_db)) -> list:
    return []
