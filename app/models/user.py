from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    passwd: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None
    
    class Config:
        extra = "ignore"

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    passwd: str
    register_date: Optional[datetime] = None
    deleted: bool
    active: bool

    class Config:
        from_atributes = True

class UsersPaginationResponse(BaseModel):
    page: int
    page_size: int
    total: int
    users: List[User]

class UsersCountResponse(BaseModel):
    total_users: int
