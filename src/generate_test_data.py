import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Organization, Storage, Fullness, WasteType
from database import get_db


async def generate_test_data(session: AsyncSession):
    waste_types = [
        WasteType(name="Стекло"),
        WasteType(name="Пластик"),
        WasteType(name="Биоотходы"),
    ]

    session.add_all(waste_types)
    await session.commit()

    organizations = [
        Organization(name="Организация 1", latitude=55.7558, longitude=37.6173),
        Organization(name="Организация 2", latitude=55.7512, longitude=37.6180),
    ]

    session.add_all(organizations)
    await session.commit()

    storages = [
        Storage(name="Хранилище 1", latitude=55.7600, longitude=37.6155),
        Storage(name="Хранилище 2", latitude=55.7620, longitude=37.6200),
    ]

    for storage in storages:
        fullness_records = [
            Fullness(organization_id=None, storage_id=storage.id,
                     waste_type_id=random.choice([waste.id for waste in waste_types]),
                     current_fill=random.randint(0, 100), capacity=100)
            for _ in range(len(waste_types))
        ]
        storage.fullness = fullness_records

    session.add_all(storages)
    await session.commit()


async def main():
    async for session in get_db():
        await generate_test_data(session)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())