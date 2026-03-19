import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.user.repository import SQLAlchemyUserRepository
from typing import Optional, List
from src.models.user import User  
from src.core.security import hash_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db 
        self.repository = SQLAlchemyUserRepository(db)

    async def get_user(self, user_id: str) -> Optional[User]:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        users = await self.repository.get_all(email=email)
        return users[0] if users else None
    
    async def get_all_users(self, **filters) -> List[User]:
        return await self.repository.get_all(**filters)

    async def create_user(self, data: dict) -> Optional[User]:
        existing_users = await self.repository.get_all(email=data['email'])
        if existing_users:
            raise ValueError("Email уже занят")
        
        hashed_password = hash_password(data['password'])
        
        user = await self.repository.create({
            "id": str(uuid.uuid4()),
            "email": data['email'],
            "hashed_password": hashed_password
        })
        return user

    async def update_user(self, user_id: str, data: dict) -> Optional[User]:
        if 'password' in data:
            data['hashed_password'] = hash_password(data['password'])
            del data['password']
        
        return await self.repository.update(user_id, data)
    
    async def delete_user(self, user_id: str) -> bool:
        return await self.repository.delete(user_id)
    
