from abc import ABC, abstractmethod
from typing import Optional, List
from src.models.chat import Chat


class IChatRepository(ABC):

    @abstractmethod
    async def get_by_id(self, chat_id: str) -> Optional[Chat]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_user_chats(self, user_id: str) -> List[Chat]:
        raise NotImplementedError
    
    @abstractmethod
    async def create(self, data: dict) -> Chat:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, chat_id: str, data: dict) -> Optional[Chat]:
        raise NotImplementedError
    
    @abstractmethod 
    async def delete(self, chat_id: str) -> bool:
        raise NotImplementedError 
    

class IChatService(ABC):

    @abstractmethod
    async def create_chat(self, user_id: str, title: str = None) -> Chat:
        raise NotImplementedError
    
    @abstractmethod
    async def get_chat(self, chat_id: str, user_id: str) -> Optional[Chat]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_user_chats(self, user_id: str) -> List[Chat]:
        raise NotImplementedError
    
    @abstractmethod
    async def update_chat_title(self, chat_id: str, user_id: str, title: str) -> Optional[Chat]:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_chat(self, chat_id: str, user_id: str) -> bool: 
        raise NotImplementedError