from pydantic import BaseModel, model_validator

from src.schemas.fullness import FullnessDTO


class OrganizationRetrieveDTO(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    # fullness: list[FullnessDTO]

    class Config:
        from_attributes = True


class OrganizationIdDTO(BaseModel):
    id: int

    class Config:
        from_attributes = True


class OrganizationCreateDTO(BaseModel):
    name: str
    latitude: float
    longitude: float


class OrganizationUpdateDTO(BaseModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    @model_validator(mode="before")
    def at_least_one_field(cls, values):
        if not any(values.get(field) is not None for field in ('name', 'latitude', 'longitude')):
            raise ValueError("At least one field (name, latitude, or longitude) must be provided")
        return values
