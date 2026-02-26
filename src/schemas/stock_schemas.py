from pydantic import BaseModel
from typing import Optional
import datetime

class StockBase(BaseModel):
    description: str

class StockCreate(StockBase):
    pass

class StockUpdate(BaseModel):
    description: Optional[str] = None

class StockRead(StockBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
    class Config:
        from_attributes = True
        validate_by_name = True


class StockReport(BaseModel):
    product_id: int
    description: str
    quantity: int
    unit_price: float
    total_value: float

    class Config:
        from_attributes = True
