from pydantic import BaseModel
from typing import Optional
import datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserRead(UserBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
