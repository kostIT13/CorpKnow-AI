from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime


class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True  
    )