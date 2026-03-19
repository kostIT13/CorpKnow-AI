from pydantic import BaseModel
from typing import Optional, List 
from datetime import datetime


class ChatCreate(BaseModel):
    title: Optional[str] = "Новый чат"

class ChatResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

class ChatListResponse(BaseModel):
    chats: List[ChatResponse]
    total: int

class MessageCreate(BaseModel):
    chat_id: str
    query: str

class MessageResponse(BaseModel): 
    id: str
    role: str 
    content: str
    created_at: datetime

class ChatCompletionRequest(BaseModel):
    query: str
    chat_id: str
    k: int = 3

class ChatCompletionResponse(BaseModel): 
    answer: str
    sources: List[str]
    chat_id: str