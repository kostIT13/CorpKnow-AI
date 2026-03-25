from src.services.document.repository import SQLAlchemyDocumentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from src.models.document import Document, DocumentStatus
import hashlib
import uuid
import os
from pathlib import Path
from datetime import datetime, timezone


class DocumentService:
    def __init__(self, db: AsyncSession, upload_dir: str = 'uploads'):
        self.db = db 
        self.repository = SQLAlchemyDocumentRepository(db)
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def get_document_by_id(self, document_id: str, user_id: str) -> Optional[Document]:
        document = await self.repository.get_by_id(document_id)
        if document and document.user_id != user_id:
            return None
        return document
    
    async def get_user_documents(self, user_id: str) -> List[Document]:
        return await self.repository.get_user_documents(user_id)

    async def upload_document(
        self, 
        user_id: str, 
        filename: str, 
        file_content: bytes,
        file_type: str
    ) -> Document:
        allowed_types = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if file_type not in allowed_types:
            raise ValueError(f"Неподдерживаемый тип файла: {file_type}")

        content_hash = hashlib.sha256(file_content).hexdigest()
        
        existing = await self._check_duplicate(user_id, content_hash)
        if existing:
            return existing

        file_id = str(uuid.uuid4())
        ext = Path(filename).suffix or ".bin"
        file_path = self.upload_dir / f"{file_id}{ext}"
        
        now = datetime.now(timezone.utc)

        with open(file_path, "wb") as f:
            f.write(file_content)
        doc = await self.repository.create({
            "id": file_id,
            "user_id": user_id,
            "filename": filename,
            "file_path": str(file_path),
            "file_size": len(file_content),
            "file_type": file_type,
            "content_hash": content_hash,
            "status": DocumentStatus.PENDING,
            "chunk_count": 0,
            "created_at": now,
            "updated_at": now
            
        })
        
        return doc

    async def _check_duplicate(self, user_id: str, content_hash: str) -> Optional[Document]:
        documents = await self.repository.get_user_documents(user_id)
        for document in documents:
            if document.content_hash == content_hash and not document.is_deleted:
                return document
        return None

    async def _index_document(self, document: Document):
        pass  

    async def delete_document(self, doc_id: str, user_id: str) -> bool:
        document = await self.get_document_by_id(doc_id, user_id)
        if not document:
            return False
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        return await self.repository.delete(doc_id)
        