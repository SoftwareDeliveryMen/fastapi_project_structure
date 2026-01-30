from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
from app.utils.helpers import is_strong_password, sanitize_string, format_datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    is_active: bool = True
    
    @field_validator('username')
    @classmethod
    def sanitize_username(cls, v: str) -> str:
        return sanitize_string(v)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not is_strong_password(v):
            raise ValueError(
                'Password must contain at least 8 characters, '
                'including uppercase, lowercase, and a number'
            )
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    
    @field_validator('username')
    @classmethod
    def sanitize_username(cls, v: Optional[str]) -> Optional[str]:
        return sanitize_string(v) if v else None
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: Optional[str]) -> Optional[str]:
        if v and not is_strong_password(v):
            raise ValueError(
                'Password must contain at least 8 characters, '
                'including uppercase, lowercase, and a number'
            )
        return v

class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: format_datetime
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
