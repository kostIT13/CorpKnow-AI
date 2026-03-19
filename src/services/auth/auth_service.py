from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from src.core.config import settings
from src.core.security import verify_password  
from src.services.user.user_service import UserService
from src.models.user import User


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        from src.core.security import hash_password 
        return hash_password(password)

    def create_access_token(self, data: dict, expires_delta: Optional[int] = None) -> str:
        to_encode = data.copy()
        
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        
        return encoded_jwt

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.user_service.get_user_by_email(email)
        
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        return user