from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from src.models.document import Document, DocumentStatus
from src.services.document.repository import SQLAlchemyDocumentRepository
from pathlib import Path
import hashlib
import uuid
import os
import asyncio
import logging
from datetime import datetime, timezone
from src.core.database import engine


logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self, db: AsyncSession, upload_dir: str = 'uploads'):
        self.db = db 
        self.repository = SQLAlchemyDocumentRepository(db)
        self.engine = engine
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"DocumentService инициализирован (upload_dir={self.upload_dir})")

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
        
        allowed_types = [
            "application/pdf", 
            "text/plain", 
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]
        if file_type not in allowed_types:
            raise ValueError(f"Неподдерживаемый тип файла: {file_type}")

        if len(file_content) == 0:
            raise ValueError("Пустой файл не может быть загружен")

        content_hash = hashlib.sha256(file_content).hexdigest()
        
        existing = await self._check_duplicate(user_id, content_hash)
        if existing:
            logger.info(f"Найден дубликат документа: {existing.filename}")
            return existing

        file_id = str(uuid.uuid4())
        ext = Path(filename).suffix or ".bin"
        file_path = self.upload_dir / f"{file_id}{ext}"
        
        try:
            with open(file_path, "wb") as f:
                f.write(file_content)
            logger.info(f"Файл сохранён: {file_path} ({len(file_content)} байт)")
        except IOError as e:
            logger.error(f"Ошибка записи файла {file_path}: {e}")
            raise ValueError(f"Не удалось сохранить файл: {e}")

        now = datetime.now(timezone.utc)
        
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
        
        logger.info(f"Документ создан в БД: {doc.id} ({doc.filename})")
        
        asyncio.create_task(self._index_document_in_background(doc.id, doc.user_id))
        
        return doc

    async def _check_duplicate(self, user_id: str, content_hash: str) -> Optional[Document]:
        documents = await self.repository.get_user_documents(user_id)
        for document in documents:
            if document.content_hash == content_hash and not document.is_deleted:
                return document
        return None


    async def _index_document_in_background(self, document_id: str, user_id: str):
        async with AsyncSession(self.engine) as session:
            try:
                logger.info(f"[INDEX] Начинаю индексацию (id={document_id})")
            
                from src.services.document.repository import SQLAlchemyDocumentRepository
                repo = SQLAlchemyDocumentRepository(session)
                document = await repo.get_by_id(document_id)
            
                if not document:
                    logger.error(f"Документ {document_id} не найден в БД")
                    return
            
                from src.services.rag.rag_service import rag_service
            
                success = await rag_service.index_document(document, db_session=session)
            
                if success:
                    await session.commit()  
                    logger.info(f"[INDEX] Документ {document_id} проиндексирован и статус ОБНОВЛЁН (COMMIT)")
                else:
                    await session.rollback()
                    logger.error(f"[INDEX] Индексация {document_id} вернула False")
                
            except ImportError as e:
                logger.warning(f"[INDEX] RAG-сервис недоступен: {e}")
            except Exception as e:
                logger.error(f"[INDEX] Ошибка индексации {document_id}: {type(e).__name__}: {e}", exc_info=True)
  

    async def _index_document(self, document: Document):
        logger.info(f"[MANUAL] Индексация {document.filename} (id={document.id})")
        from src.services.rag.rag_service import rag_service
        return await rag_service.index_document(document)

    async def delete_document(self, doc_id: str, user_id: str) -> bool:
        document = await self.get_document_by_id(doc_id, user_id)
        if not document:
            logger.warning(f"Документ {doc_id} не найден или доступ запрещён")
            return False
        
        if os.path.exists(document.file_path):
            try:
                os.remove(document.file_path)
                logger.info(f"Файл удалён: {document.file_path}")
            except OSError as e:
                logger.error(f"Ошибка удаления файла {document.file_path}: {e}")
        
        try:
            from src.services.rag.rag_service import rag_service
            await rag_service.delete_document_from_index(doc_id, user_id)
            logger.info(f"Документ {doc_id} удалён из индекса")
        except ImportError:
            logger.warning("RAG-сервис недоступен, пропуск удаления из индекса")
        except Exception as e:
            logger.error(f"Ошибка удаления из индекса: {e}")
        
        result = await self.repository.delete(doc_id)
        if result:
            logger.info(f"Документ {doc_id} удалён из БД")
        return result