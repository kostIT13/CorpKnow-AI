from sqlalchemy.ext.asyncio import AsyncSession
from src.services.chat.repository import SQLAlchemyChatRepository
from typing import Optional, List
from src.models.chat import Chat
from uuid import uuid4
from src.services.chat.base import IChatService
from datetime import datetime, timezone
from sqlalchemy import select
from src.models.message import Message


class ChatService(IChatService):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = SQLAlchemyChatRepository(db)

    async def get_chat(self, chat_id: str, user_id: str) -> Optional[Chat]:
        chat = await self.repository.get_by_id(chat_id)
        if chat and chat.user_id != user_id:
            return None
        return chat
    
    async def get_user_chats(self, user_id: str) -> List[Chat]:
        return await self.repository.get_user_chats(user_id)
    
    async def create_chat(self, user_id: str, title: str = 'Новый чат') -> Chat:
        return await self.repository.create({"id": str(uuid4()), "user_id": user_id, "title": title, "created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)})
    
    async def update_chat_title(self, chat_id: str, user_id: str, title: str) -> Optional[Chat]:
        chat = await self.get_chat(chat_id, user_id)
        if not chat:
            return None
        
        return await self.repository.update(chat_id, {"title": title})
    
    async def delete_chat(self, chat_id: str, user_id: str) -> bool:
        chat = await self.get_chat(chat_id, user_id)
        if not chat:
            return False
        
        return await self.repository.delete(chat_id)

    async def add_message(
        self,
        chat_id: str,
        role: str,
        content: str,
        metadata_: Optional[dict] = None
    ) -> Message:
        message = Message(
            id=str(uuid4()),
            chat_id=chat_id,
            role=role,
            content=content,
            metadata_=metadata_ or {},
            is_starred=False
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message
    
    async def get_chat_messages(self, chat_id: str) -> List[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
        )
        return list(result.scalars().all())