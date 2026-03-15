from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base
from sqlalchemy import String, DateTime, func
from datetime import datetime 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.chat import Chat

class User(Base):   
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    chats: Mapped[list["Chat"]] = relationship(
        "Chat", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )