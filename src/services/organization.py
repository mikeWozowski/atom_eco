from src.repositories.fullness import FullnessRepository
from src.repositories.organization import OrganizationRepository
from src.schemas.organization import OrganizationRetrieveDTO


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
        return [OrganizationRetrieveDTO.from_orm(org) for org in organizations]

    async def create_organization(self) -> OrganizationRetrieveDTO:
        ...
