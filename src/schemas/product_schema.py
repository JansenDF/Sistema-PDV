from pydantic import BaseModel
from typing import Optional
import datetime

class ProductBase(BaseModel):
    description: str
    quantity: int

class ProductCreate(ProductBase):
    stock_id: int

class ProductUpdate(BaseModel):
    description: str

class ProductRead(ProductBase):
    id: int
    stock_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
    class Config:
        from_attributes = True
        validate_by_name = True
