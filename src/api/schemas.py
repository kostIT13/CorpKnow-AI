from pydantic import BaseModel, EmailStr
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

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

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

class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_size: int
    file_type: Optional[str] = None
    status: str
    chunk_count: Optional[int] = 0
    created_at: datetime

class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    status: str
    message: str = "Документ загружен и обрабатывается"