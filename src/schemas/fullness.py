from pydantic import BaseModel, conlist


class FullnessDTO(BaseModel):
    waste_type_name: str
    remaining_space: int | None = None
    current_fill: int
    capacity: int

    class Config:
        from_attributes = True

class FullnessCreateDTO(BaseModel):
    waste_type_id: int
    current_fill: int = 0
    capacity: int

