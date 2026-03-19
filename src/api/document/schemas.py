from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_size: int
    file_type: Optional[str] = None
    status: str
    chunk_count: Optional[int] = 0
    created_at: datetime

class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    status: str
    message: str = "Документ загружен и обрабатывается"