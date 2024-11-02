from pydantic import BaseModel, conlist


class FullnessDTO(BaseModel):
    waste_type_id: int
    name: str
    current_fill: int
    capacity: int

class FullnessCreateDTO(BaseModel):
    waste_type_id: int
    current_fill: int = 0
    capacity: int

