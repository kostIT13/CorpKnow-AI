from src.services.rag.chroma_client import chroma_client
from src.services.rag.embedding_service import embedding_service
from src.services.rag.document_processor import document_processor
from src.services.rag.ollama_client import ollama_client
from src.models.document import Document, DocumentStatus
from typing import List, Optional
from datetime import datetime, timezone
import logging
import asyncio
from src.services.document.repository import SQLAlchemyDocumentRepository


logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self, db_session):
        self.chroma = chroma_client
        self.db_session = db_session
        self.doc_repository = SQLAlchemyDocumentRepository(db_session)
        self.embeddings = embedding_service
        self.processor = document_processor
        self.llm = ollama_client
    
    async def index_document(self, document: Document) -> bool:
        try:
            chunks = self.processor.process(document.file_path, document.file_type)
            
            if not chunks:
                raise ValueError("Документ пуст или не удалось извлечь текст")
            
            collection = self.chroma.get_or_create_collection(document.user_id)
            
            texts = [chunk.page_content for chunk in chunks]
            embeddings = self.embeddings.embed_texts(texts)
            
            collection.add(
                ids=[f"{document.id}_{i}" for i in range(len(chunks))],
                embeddings=embeddings,
                documents=texts,
                metadatas=[
                    {
                        "document_id": document.id,
                        "filename": document.filename,
                        "chunk_index": i,
                        "user_id": document.user_id
                    }
                    for i in range(len(chunks))
                ]
            )
            
            document.status = DocumentStatus.COMPLETED
            document.chunk_count = len(chunks)
            document.processed_at = datetime.now(timezone.utc)

            await self.doc_repository.update(document.id, {
                "status": DocumentStatus.COMPLETED,
                "chunk_count": len(chunks),
                "processed_at": datetime.now(timezone.utc)
            })
            
            logger.info(f"Документ {document.id} проиндексирован ({len(chunks)} чанков)")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка индексации {document.id}: {e}")
            document.status = DocumentStatus.FAILED
            document.error_message = str(e)

            await self.doc_repository.update(document.id, {
                "status": DocumentStatus.FAILED,
                "error_message": str(e)
            })

            return False
    
    async def search(
        self,
        query: str,
        user_id: str,
        top_k: int = 5
    ) -> List[dict]:
        try:
            query_embedding = self.embeddings.embed_text(query)
            
            collection = self.chroma.get_or_create_collection(user_id)
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            relevant_chunks = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    relevant_chunks.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "score": 1 - results["distances"][0][i] if results["distances"] else 0
                    })
            
            logger.info(f"Найдено {len(relevant_chunks)} релевантных чанков")
            return relevant_chunks
            
        except Exception as e:
            logger.error(f"Ошибка поиска: {e}")
            return []
    
    async def generate_answer(
        self,
        query: str,
        user_id: str,
        chat_history: Optional[List[dict]] = None
    ) -> dict:
        relevant_chunks = await self.search(query, user_id, top_k=5)
        
        if not relevant_chunks:
            return {
                "answer": "К сожалению, я не нашёл информации по вашему вопросу в загруженных документах. Попробуйте загрузить документы или перефразировать вопрос.",
                "sources": [],
                "used_chunks": []
            }
        
        context = "\n\n".join([
            f"[Источник: {chunk['metadata'].get('filename', 'Unknown')}]\n{chunk['content']}"
            for chunk in relevant_chunks
        ])
        
        system_prompt = """Ты — умный помощник компании CorpKnow AI.
Отвечай на вопросы ТОЛЬКО на основе предоставленного контекста.
Если ответа нет в контексте — честно скажи, что не знаешь.
Отвечай на русском языке."""
        
        user_prompt = f"""Контекст из документов:
{context}

Вопрос пользователя: {query}

Ответ:"""
        
        answer = await asyncio.to_thread(
            self.llm.generate,
            prompt=user_prompt,
            system=system_prompt
        )
        
        sources = list(set([
            chunk["metadata"].get("filename", "Unknown")
            for chunk in relevant_chunks
        ]))
        
        return {
            "answer": answer,
            "sources": sources,
            "used_chunks": relevant_chunks
        }
    
    async def delete_document_from_index(self, document_id: str, user_id: str):
        try:
            collection = self.chroma.get_or_create_collection(user_id)
            
            results = collection.get(
                where={"document_id": document_id},
                include=[]
            )
            
            if results["ids"]:
                collection.delete(ids=results["ids"])
                logger.info(f"Документ {document_id} удалён из индекса")
            
        except Exception as e:
            logger.error(f"Ошибка удаления из индекса: {e}")

