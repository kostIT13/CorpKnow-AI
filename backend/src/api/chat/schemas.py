from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


class ChatCreate(BaseModel):
    title: Optional[str] = Field(default="Новый чат", min_length=1, max_length=255)


class ChatUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class ChatMessageRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000)
    chat_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    role: str 
    content: str
    sources: Optional[List[str]] = None  
    chat_id: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ChatListResponse(BaseModel):
    id: str
    title: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    sources: Optional[List[str]] = []
    created_at: datetime
    is_starred: bool
    
    model_config = ConfigDict(from_attributes=True)

class ChatBaseResponse(BaseModel):
    id: str
    title: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class ChatResponse(BaseModel):
    id: str
    title: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []  
    
    model_config = ConfigDict(from_attributes=True)