from pydantic import BaseModel
from typing import Optional
import datetime

class ProductCategoryBase(BaseModel):
    description: str

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategoryUpdate(BaseModel):
    description: str

class ProductCategoryRead(ProductCategoryBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
    class Config:
        from_attributes = True
        validate_by_name = True
