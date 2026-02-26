from pydantic import BaseModel
from typing import Optional
import datetime

class SupplierBase(BaseModel):
    company_name: str

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    company_name: str

class SupplierRead(SupplierBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
    class Config:
        from_attributes = True
        validate_by_name = True
