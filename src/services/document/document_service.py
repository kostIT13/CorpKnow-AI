from src.services.document.repository import SQLAlchemyDocumentrepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from src.models.document import Document


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db 
        self.repository = SQLAlchemyDocumentrepository

    async def get_document_by_id(self, document_id: str) -> Optional[Document]:
        return await self.repository.get_by_id(document_id)
    
    async def get_user_documents(self, user_id: str) -> List[Document]:
        return 