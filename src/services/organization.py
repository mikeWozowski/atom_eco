from fastapi import HTTPException

from src.schemas.fullness import FullnessCreateDTO, FullnessDTO
from src.repositories.fullness import FullnessRepository
from src.repositories.organization import OrganizationRepository
from src.schemas.organization import OrganizationRetrieveDTO, OrganizationIdDTO, OrganizationCreateDTO


class OrganizationService:
    def __init__(
            self,
            organization_repository: OrganizationRepository,
            fullness_repository: FullnessRepository
    ) -> None:
        self.organization_repository = organization_repository
        self.fullness_repository = fullness_repository

    async def get_organizations(self):
        organizations = await self.organization_repository.get_all_organizations()

        return [
            OrganizationRetrieveDTO(
                id=organization.id,
                name=organization.name,
                latitude=organization.latitude,
                longitude=organization.longitude,
                fullness=[
                    FullnessDTO(
                        id=fullness.id,
                        waste_type_name=fullness.waste_type.name,
                        current_fill=fullness.current_fill,
                        capacity=fullness.capacity
                    )
                    for fullness in organization.fullness
                ]
            )
            for organization in organizations
        ]

    async def get_organization_by_id(self, organization_id: int) -> OrganizationRetrieveDTO:
        organization = await self.organization_repository.get_organization_by_id(organization_id)

        if organization is None:
            raise HTTPException(status_code=404, detail="Organization not found")

        return OrganizationRetrieveDTO(
            id=organization.id,
            name=organization.name,
            latitude=organization.latitude,
            longitude=organization.longitude,
            fullness=[
                FullnessDTO(
                    id=fullness.id,
                    waste_type_name=fullness.waste_type.name,
                    current_fill=fullness.current_fill,
                    capacity=fullness.capacity
                )
                for fullness in organization.fullness
            ]
        )

    async def create_organization(
            self,
            organization_create_dto: OrganizationCreateDTO,
            fullness_create_dto: list[FullnessCreateDTO]
    ) -> OrganizationIdDTO:
        if not fullness_create_dto:
            raise ValueError("Fullness data must not be empty")

        organization = await self.organization_repository.create_organization(organization_create_dto)

        for fullness in fullness_create_dto:
            await self.fullness_repository.create_fullness(
                fullness,
                organization_id=organization.id
            )

        return organization

    async def delete_organization_by_id(self, organization_id: int):
        organization = await self.organization_repository.get_organization_by_id(organization_id)

        if organization is None:
            raise HTTPException(status_code=404, detail="Organization not found")

        await self.organization_repository.delete_organization_by_id(organization_id)

    async def fill_waste(self, organization_id: int, waste_type_id: int, amount: int):
        fullness = await self.fullness_repository.get_fullness_by_organization_id(organization_id, waste_type_id)

        if fullness is None:
            return {"message": "No fullness record found for this waste type."}

        available_space = fullness.capacity - fullness.current_fill

        if available_space < amount:
            shortage = amount - available_space
            return {
                "message": f"Insufficient space. You are short of {shortage} units. We recommend sending the waste for recycling."
            }

        new_fill = fullness.current_fill + amount
        await self.fullness_repository.update_fullness(fullness.id, new_fill)

        remaining_space = fullness.capacity - new_fill
        return {
            "message": f"Waste added successfully. Remaining space for waste type {waste_type_id}: {remaining_space} units."
        }
