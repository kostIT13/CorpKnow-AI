from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base  
from sqlalchemy import String, ForeignKey, Text, Boolean, func, DateTime
from typing import Optional, TYPE_CHECKING
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

if TYPE_CHECKING:
    from src.models.chat import Chat


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    chat_id: Mapped[str] = mapped_column(String(36), ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict, nullable=True)
    is_starred: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")