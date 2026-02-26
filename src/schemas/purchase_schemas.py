from pydantic import BaseModel
from typing import Optional
import datetime

class Items(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class PurchaseBase(BaseModel):
    supplier_id: int
    stock_id: int
    items: list[Items]


class PurchaseCreate(PurchaseBase):
    pass


class PurchaseUpdate(BaseModel):
    supplier_id: Optional[int] = None
    stock_id: Optional[int] = None
    items: Optional[list[Items]] = None


class PurchaseRead(PurchaseBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
    

    class Config:
        from_attributes = True
        validate_by_name = True
