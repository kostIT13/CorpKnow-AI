from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from src.core.database import get_db
from src.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from src.services.user.user_service import UserService
from typing import Annotated
from jose import JWTError, jwt
from src.models.user import User


async def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    user_service: UserServiceDependency,
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные учётные данные",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_service.get_user(user_id)
    if user is None:
        raise credentials_exception
    
    return user

CurrentUserDependency = Annotated[User, Depends(get_current_user)]