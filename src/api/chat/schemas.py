# src/api/chat/schemas.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


class ChatCreate(BaseModel):
    title: Optional[str] = Field(default="Новый чат", min_length=1, max_length=255)


class ChatUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class ChatMessageRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000)


class ChatMessageResponse(BaseModel):
    role: str 
    content: str
    sources: Optional[List[str]] = None  
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ChatResponse(BaseModel):
    id: str
    title: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse] = []  
    
    model_config = ConfigDict(from_attributes=True)


class ChatListResponse(BaseModel):
    id: str
    title: str
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)