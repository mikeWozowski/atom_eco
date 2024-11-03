from pydantic import BaseModel, model_validator

from src.schemas.fullness import FullnessDTO


class StorageRetrieveDTO(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    fullness: list[FullnessDTO]

    class Config:
        from_attributes = True


class StorageAdvancedRetrieveDTO(BaseModel):
    id: int
    name: str
    fullness: list[FullnessDTO]
    distance: float

    class Config:
        from_attributes = True


class StorageIdDTO(BaseModel):
    id: int

    class Config:
        from_attributes = True


class StorageCreateDTO(BaseModel):
    name: str
    latitude: float
    longitude: float


class StorageUpdateDTO(BaseModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    @model_validator(mode="before")
    def at_least_one_field(cls, values):
        if not any(values.get(field) is not None for field in ('name', 'latitude', 'longitude')):
            raise ValueError("At least one field (name, latitude, or longitude) must be provided")
        return values
