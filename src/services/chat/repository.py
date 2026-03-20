from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from src.models.chat import Chat
from sqlalchemy import select
from datetime import datetime, timezone  
from src.services.chat.base import IChatRepository


class SQLAlchemyChatRepository(IChatRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, chat_id: str) -> Optional[Chat]: 
        result = await self.session.get(Chat, chat_id)  
        return result
    
    async def get_user_chats(self, user_id: str) -> List[Chat]:
        query = select(Chat).where(Chat.user_id == user_id).order_by(Chat.updated_at.desc())
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def create(self, data: dict) -> Chat: 
        chat = Chat(**data)
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat
    
    async def update(self, chat_id: str, data: dict) -> Optional[Chat]: 
        chat = await self.get_by_id(chat_id)
        if not chat:
            return None
        
        for field, value in data.items():
            if hasattr(chat, field):
                setattr(chat, field, value)
        
        chat.updated_at = datetime.now(timezone.utc) 
        await self.session.commit()
        await self.session.refresh(chat)
        return chat
    
    async def delete(self, chat_id: str) -> bool:
        chat = await self.get_by_id(chat_id)
        if not chat:
            return False
        
        await self.session.delete(chat)
        await self.session.commit()
        return True