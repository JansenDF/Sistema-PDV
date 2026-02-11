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
        orm_mode = True
        allow_population_by_field_name = True
