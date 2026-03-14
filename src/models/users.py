from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base
from sqlalchemy import String, DateTime, func
from datetime import datetime 


class User(Base):
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())