from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date, datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    nickname: Optional[str] = None
    about_me: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[date] = None
    favorites: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    about_me: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[date] = None
    favorites: Optional[str] = None

class UserPatch(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    about_me: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[date] = None
    favorites: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Authentication schemas
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None 