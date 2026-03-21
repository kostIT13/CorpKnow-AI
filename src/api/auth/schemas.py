from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from typing import List, Optional
from datetime import datetime
import re


class UserRegister(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Неверный формат email')
        return v.lower()
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Пароль не может быть длиннее 72 байт')
        return v

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True  
    )