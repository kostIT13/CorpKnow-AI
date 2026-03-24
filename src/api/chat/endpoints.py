from fastapi import APIRouter, status, HTTPException
from src.api.auth.dependencies import CurrentUserDependency
from src.api.chat.dependencies import ChatServiceDependency, ChatDependency
from src.api.chat.schemas import ChatCreate, ChatListResponse, ChatMessageRequest, ChatMessageResponse, ChatResponse, ChatUpdate, ChatBaseResponse
from typing import List, Optional
from datetime import datetime, timezone



router = APIRouter(prefix='/chats', tags=["Chats"])

@router.get('/', response_model=List[ChatListResponse])
async def get_user_chats(current_user: CurrentUserDependency, service: ChatServiceDependency):
    chats = await service.get_user_chats(current_user.id)
    return chats

@router.post('/', response_model=ChatListResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(data: ChatCreate, current_user: CurrentUserDependency, service: ChatServiceDependency):
    chat = await service.create_chat(user_id=current_user.id, title=data.title)
    return chat 

@router.get('/{chat_id}', response_model=ChatBaseResponse)
async def get_chat(chat: ChatDependency):
    return chat 

@router.patch('/{chat_id}', response_model=ChatBaseResponse)
async def update_chat(data: ChatUpdate, chat: ChatDependency, service: ChatServiceDependency):
    updated_chat = await service.update_chat_title(chat_id=chat.id, user_id=chat.user_id, title=data.title)
    return updated_chat

@router.delete('/{chat_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat: ChatDependency, service: ChatServiceDependency):
    await service.delete_chat(chat_id=chat.id, user_id=chat.user_id)
    return None

rag_router = APIRouter(prefix='/chat', tags=["RAG"])

@rag_router.post("/completions", response_model=ChatMessageResponse)
async def chat_completion(
    data: ChatMessageRequest,
    current_user: CurrentUserDependency,
    chat_service: ChatServiceDependency,
    chat_id: Optional[str] = None 
):
    if chat_id:
        chat = await chat_service.get_chat(chat_id, current_user.id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Чат не найден"
            )

    return ChatMessageResponse(
        role="assistant",
        content=f"RAG-ответ на: {data.query}\n\n(Здесь будет интеграция с LangChain + ChromaDB)",
        sources=["document_1.pdf", "document_2.md"],
        created_at=datetime.now(timezone.utc)
    )
