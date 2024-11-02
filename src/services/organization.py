from src.schemas.fullness import FullnessCreateDTO
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
        return [OrganizationRetrieveDTO.model_validate(org) for org in organizations]

    async def get_organization_by_id(self, organization_id: int):
        organization = await self.organization_repository.get_organization_by_id(organization_id)
        return organization

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
