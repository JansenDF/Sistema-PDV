from pydantic import BaseModel
from typing import Optional
import datetime

class Items(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    # class Config:
    #     from_attributes = True

class SaleBase(BaseModel):
    operator_id: int
    client_id: int
    items: list[Items]

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    operator_id: Optional[int] = None
    client_id: Optional[int] = None
    items: Optional[list[Items]] = None

class SaleRead(SaleBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
    
    class Config:
        from_attributes = True
        validate_by_name = True


class SaleSummary(BaseModel):
    sale_id: int
    client_name: str
    operator_name: str
    total_value: float
    created_at: datetime.datetime

    class Config:
        from_attributes = True
