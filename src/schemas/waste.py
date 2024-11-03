from pydantic import BaseModel


class FillWasteDTO(BaseModel):
    waste_type_id: int
    amount: int
