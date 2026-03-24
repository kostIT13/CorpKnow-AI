from sqlalchemy.ext.asyncio import AsyncSession
from src.services.chat.chat_service import ChatService
from typing import Annotated
from fastapi import Depends, HTTPException, status
from src.core.database import get_db
from src.models import Chat
from src.api.auth.dependencies import CurrentUserDependency


async def get_chat_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    return ChatService(db)

ChatServiceDependency = Annotated[ChatService, Depends(get_chat_service)]

async def get_chat_or_404(
    chat_id: str,
    chat_service: ChatServiceDependency,
    current_user = CurrentUserDependency
) -> Chat:
    chat = await chat_service.get_chat(chat_id, current_user.id)
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Чат не найден или доступ запрещён"
        )
    
    return chat

ChatDependency = Annotated[Chat, Depends(get_chat_or_404)]


