from pydantic import BaseModel


class FullnessDTO(BaseModel):
    waste_type_id: int
    waste_type: str
    current_fill: int
    capacity: int


class FullnessCreateDTO(BaseModel):
    waste_type_name: str
    capacity: int
