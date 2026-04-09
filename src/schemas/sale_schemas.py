from pydantic import BaseModel
from typing import Optional
import datetime

class ProductRead(BaseModel):
    description: str

class Items(BaseModel):
    product_id: int
    product: Optional[ProductRead] = None
    quantity: int
    unit_price: float

    # class Config:
    #     from_attributes = True

class SaleBase(BaseModel):
    operator_id: int
    client_id: int
    items: list[Items]
    total_value: Optional[float] = None
    date: Optional[datetime.date]

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    operator_id: Optional[int] = None
    client_id: Optional[int] = None
    items: Optional[list[Items]] = None
    date: Optional[datetime.datetime] = None

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
    date: datetime.date

    class Config:
        from_attributes = True
