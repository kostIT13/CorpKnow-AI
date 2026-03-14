from sqlalchemy.orm import Mapped, mapped_column 
from src.core.database import Base 
from sqlalchemy import String, ForeignKey, Boolean, func, DateTime
from datetime import datetime


class Chats(Base):
    __tablename__ = "chats"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), default='Новый чат')
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())