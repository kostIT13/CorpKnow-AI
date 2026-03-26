from fastapi import APIRouter, status, HTTPException
from src.api.auth.dependencies import CurrentUserDependency
from src.api.chat.dependencies import ChatServiceDependency, ChatDependency
from src.api.chat.schemas import ChatCreate, ChatListResponse, ChatMessageRequest, ChatMessageResponse, ChatResponse, ChatUpdate, ChatBaseResponse, MessageResponse
from typing import List, Optional
from datetime import datetime, timezone
from src.services.rag.dependencies import RAGServiceDependency
import uuid


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
    rag_service: RAGServiceDependency,
):
    if data.chat_id:
        chat = await chat_service.get_chat(data.chat_id, current_user.id)
        if not chat:
            raise HTTPException(status_code=404, detail="Чат не найден")
        chat_id = data.chat_id
    else:
        chat = await chat_service.create_chat(
            user_id=current_user.id,
            title=data.query[:50]  
        )
        chat_id = chat.id
    
    await chat_service.add_message(
        chat_id=chat_id,
        role="user",
        content=data.query,
        metadata_={}
    )
    
    result = await rag_service.generate_answer(
        query=data.query,
        user_id=current_user.id
    )
    
    assistant_message = await chat_service.add_message(
        chat_id=chat_id,
        role="assistant",
        content=result["answer"],
        metadata_={"sources": result["sources"]} 
    )
    
    return ChatMessageResponse(
        role="assistant",
        content=result["answer"], 
        sources=result["sources"],
        chat_id=chat_id, 
        created_at=assistant_message.created_at
    )

@rag_router.get("/history/{chat_id}", response_model=ChatResponse)
async def get_chat_history(
    chat_id: str,
    current_user: CurrentUserDependency,
    chat_service: ChatServiceDependency
):
    chat = await chat_service.get_chat(chat_id, current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")
    
    messages = await chat_service.get_chat_messages(chat_id)
    
    return ChatResponse(
        id=chat.id,
        title=chat.title,
        user_id=chat.user_id,
        created_at=chat.created_at,
        updated_at=chat.updated_at,
        messages=[
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                sources=msg.sources,  
                created_at=msg.created_at,
                is_starred=msg.is_starred,
            )
            for msg in messages
        ]
    )