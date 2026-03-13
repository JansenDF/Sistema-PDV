from pydantic import BaseModel

class SoldBase(BaseModel):
    id: int
    description: str
    quantity: int
    total_value: float
