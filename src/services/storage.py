import math

from fastapi import HTTPException

from src.schemas.waste import FillWasteDTO
from src.schemas.storage import StorageAdvancedRetrieveDTO
from src.repositories.organization import OrganizationRepository
from src.schemas.fullness import FullnessDTO, FullnessCreateDTO
from src.schemas.storage import StorageRetrieveDTO, StorageIdDTO, StorageCreateDTO
from src.repositories.storage import StorageRepository
from src.repositories.fullness import FullnessRepository


class StorageService:
    def __init__(
            self,
            storage_repository: StorageRepository,
            fullness_repository: FullnessRepository,
            organization_repository: OrganizationRepository = None
    ) -> None:
        self.storage_repository = storage_repository
        self.fullness_repository = fullness_repository
        self.organization_repository = organization_repository

    async def get_storages(self):
        storages = await self.storage_repository.get_all_storages()

        return [
            StorageRetrieveDTO(
                id=storage.id,
                name=storage.name,
                latitude=storage.latitude,
                longitude=storage.longitude,
                fullness=[
                    FullnessDTO(
                        id=fullness.id,
                        waste_type_name=fullness.waste_type.name,
                        current_fill=fullness.current_fill,
                        capacity=fullness.capacity
                    )
                    for fullness in storage.fullness
                ]
            )
            for storage in storages
        ]

    async def get_storage_by_id(self, storage_id: int):
        storage = await self.storage_repository.get_storage_by_id(storage_id)

        if storage is None:
            raise HTTPException(status_code=404, detail="Storage not found")

        return StorageRetrieveDTO(
            id=storage.id,
            name=storage.name,
            latitude=storage.latitude,
            longitude=storage.longitude,
            fullness=[
                FullnessDTO(
                    id=fullness.id,
                    waste_type_name=fullness.waste_type.name,
                    current_fill=fullness.current_fill,
                    capacity=fullness.capacity
                )
                for fullness in storage.fullness
            ]
        )

    async def create_storage(
            self,
            storage_create_dto: StorageCreateDTO,
            fullness_create_dto: list[FullnessCreateDTO]
    ) -> StorageIdDTO:
        if not fullness_create_dto:
            raise ValueError("Fullness data must not be empty")

        storage = await self.storage_repository.create_storage(storage_create_dto)

        for fullness in fullness_create_dto:
            await self.fullness_repository.create_fullness(
                fullness,
                storage_id=storage.id
            )

        return storage

    async def delete_storage_by_id(self, storage_id: int):
        storage = await self.storage_repository.get_storage_by_id(storage_id)

        if storage is None:
            raise HTTPException(status_code=404, detail="Storage not found")

        await self.storage_repository.delete_storage_by_id(storage_id)

    async def get_storages_with_info(self, organization_id: int):
        organization = await self.organization_repository.get_organization_by_id(organization_id)
        if not organization:
            return {"message": "Organization not found."}

        storages = await self.storage_repository.get_all_storages()

        storage_info = []
        for storage in storages:
            distance = self.haversine((organization.latitude, organization.longitude),
                                      (storage.latitude, storage.longitude))

            storage_info.append(StorageAdvancedRetrieveDTO(
                id=storage.id,
                name=storage.name,
                fullness=[
                    FullnessDTO(
                        waste_type_id=fullness.waste_type_id,
                        waste_type_name=fullness.waste_type.name,
                        remaining_space=fullness.capacity - fullness.current_fill,
                        current_fill=fullness.current_fill,
                        capacity=fullness.capacity
                    )
                    for fullness in storage.fullness
                ],
                distance=distance
            ))

        return storage_info

    async def recycle_waste(self, organization_id: int, fill_waste_dto: FillWasteDTO):
        organization = await self.organization_repository.get_organization_by_id(organization_id)
        if not organization:
            return {"message": "Organization not found."}

        storages = await self.storage_repository.get_all_storages()

        closest_storage = None
        closest_distance = float('inf')

        for storage in storages:
            fullness = next((f for f in storage.fullness if f.waste_type_id == fill_waste_dto.waste_type_id), None)
            if fullness:
                available_space = fullness.capacity - fullness.current_fill
                if available_space >= fill_waste_dto.amount:
                    distance = self.haversine((organization.latitude, organization.longitude),
                                              (storage.latitude, storage.longitude))

                    if distance < closest_distance:
                        closest_distance = distance
                        closest_storage = storage

        if not closest_storage:
            return {"message": "No suitable storage found for recycling this waste type."}

        new_fill = closest_storage.fullness[
                       0].current_fill + fill_waste_dto.amount
        await self.fullness_repository.update_fullness(closest_storage.fullness[0].id, new_fill)

        fullness = await self.fullness_repository.get_fullness_by_organization_id(organization_id,
                                                                                  fill_waste_dto.waste_type_id)
        if fullness:
            new_fill_org = fullness.current_fill - fill_waste_dto.amount
            await self.fullness_repository.update_fullness(fullness.id, new_fill_org)

        return {
            "message": f"Waste successfully recycled to storage {closest_storage.name}."
        }

    def haversine(self, coord1, coord2):
        R = 6371000
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)

        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2) ** 2 +
             math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
