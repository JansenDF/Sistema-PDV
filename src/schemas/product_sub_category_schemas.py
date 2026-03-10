from pydantic import BaseModel
from typing import Optional
import datetime

class ProductSubCategoryBase(BaseModel):
    description: str
    product_category_id: int

class ProductSubCategoryCreate(ProductSubCategoryBase):
    pass

class ProductCategoryRead(BaseModel):
    description: str

class ProductSubCategoryUpdate(BaseModel):
    description: str

class ProductSubCategoryRead(ProductSubCategoryBase):
    id: int
    product_category: ProductCategoryRead
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
    class Config:
        from_attributes = True
        validate_by_name = True
