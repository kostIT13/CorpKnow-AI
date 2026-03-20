from sqlalchemy.ext.asyncio import AsyncSession
from src.services.chat.repository import SQLAlchemyChatRepository
from typing import Optional, List
from src.models.chat import Chat
from uuid import uuid4
from src.services.chat.base import IChatService


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
        return await self.repository.create({"id": str(uuid4()), "user_id": user_id, "title": title})
    
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
