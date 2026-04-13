from pydantic import BaseModel
from typing import Optional
import datetime


class Product(BaseModel):
    description: str


class Stock(BaseModel):
    description: str


class Supplier(BaseModel):
    company_name: str

class Items(BaseModel):
    product_id: int
    product: Product
    quantity: int
    unit_price: float


class PurchaseBase(BaseModel):
    supplier_id: int
    stock_id: int
    supplier: Supplier
    stock: Stock
    total_value: Optional[float] = None
    items: list[Items]


class ItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class PurchaseCreate(BaseModel):
    supplier_id: int
    stock_id: int
    items: list[ItemCreate]



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
