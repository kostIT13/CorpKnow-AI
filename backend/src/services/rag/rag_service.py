# src/services/rag/rag_service.py
from src.services.rag.chroma_client import chroma_client
from src.services.rag.embedding_service import embedding_service
from src.services.rag.document_processor import document_processor
from src.services.rag.ollama_client import ollama_client
from src.models.document import Document, DocumentStatus
from typing import List, Optional
from datetime import datetime, timezone
import logging
import asyncio


logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self, db_session=None):
        self.db_session = db_session
        self.chroma = chroma_client
        self.embeddings = embedding_service
        self.processor = document_processor
        self.llm = ollama_client
        self.doc_repository = None
        
        logger.info("RAGService инициализирован")
    
    async def _get_repository(self, db_session=None):
        session = db_session or self.db_session
        if session and not self.doc_repository:
            from src.services.document.repository import SQLAlchemyDocumentRepository
            self.doc_repository = SQLAlchemyDocumentRepository(session)
        return self.doc_repository
    
    async def index_document(self, document: Document, db_session=None) -> bool:
        session = db_session or self.db_session
        
        try:
            logger.info(f"[INDEX] Начинаю индексацию {document.filename} (id={document.id})")
            chunks = self.processor.process(document.file_path, document.file_type)
            
            if not chunks:
                raise ValueError("Документ пуст или не удалось извлечь текст")
            
            logger.info(f"Загружено и разбито на {len(chunks)} чанков")
            
            collection = self.chroma.get_or_create_collection(document.user_id)
            
            texts = [chunk.page_content for chunk in chunks]
            embeddings = self.embeddings.embed_texts(texts)
            
            logger.info(f"Создано {len(embeddings)} эмбеддингов")
            
            collection.add(
                ids=[f"{document.id}_{i}" for i in range(len(chunks))],
                embeddings=embeddings,
                documents=texts,
                metadatas=[
                    {
                        "document_id": document.id,
                        "filename": document.filename,
                        "chunk_index": i,
                        "user_id": document.user_id,
                        "source": chunk.metadata.get("source", document.filename)
                    }
                    for i, chunk in enumerate(chunks)
                ]
            )
            
            logger.info(f"Добавлено {len(chunks)} чанков в коллекцию user_{document.user_id}")
            
            if session:
                repository = await self._get_repository(session)
                if repository:
                    await repository.update(document.id, {
                        "status": DocumentStatus.COMPLETED,
                        "chunk_count": len(chunks),
                        "processed_at": datetime.now(timezone.utc)
                    })
                    logger.info(f"Статус документа {document.id} обновлён на COMPLETED")
            
            logger.info(f"Документ {document.id} проиндексирован ({len(chunks)} чанков)")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка индексации {document.id}: {type(e).__name__}: {e}", exc_info=True)
            
            if session:
                try:
                    repository = await self._get_repository(session)
                    if repository:
                        await repository.update(document.id, {
                            "status": DocumentStatus.FAILED,
                            "error_message": str(e)
                        })
                        logger.info(f"Статус документа {document.id} обновлён на FAILED")
                except Exception as update_error:
                    logger.error(f"Не удалось обновить статус на FAILED: {update_error}")
            
            return False
    
    async def search(
    self,
    query: str,
    user_id: str,
    top_k: int = 20  # 🔹 Увеличили с 5 до 20
    ) -> List[dict]:
    
        try:
            logger.info(f"🔍 ПОИСК: запрос='{query[:50]}...', user_id={user_id}, top_k={top_k}")
        
            query_embedding = self.embeddings.embed_text(query)
            collection = self.chroma.get_or_create_collection(user_id)
        
        # 🔹 Берём больше кандидатов для разнообразия
            results = collection.query(
            query_embeddings=[query_embedding],
                n_results=top_k * 2,  # 🔹 40 кандидатов
                include=["documents", "metadatas", "distances"]
            )
        
        # 🔹 Дедупликация: не более 3 чанков из одного документа
            seen_docs = {}
            deduplicated = []
        
            if results.get("documents") and results["documents"][0]:
                for i, doc_content in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
                    distance = results["distances"][0][i] if results.get("distances") else None
                    filename = metadata.get("filename", "Unknown")
                
                # 🔹 Ограничиваем чанки из одного файла
                    doc_count = seen_docs.get(filename, 0)
                    if doc_count < 3:  # 🔹 Макс 3 чанка из одного документа
                        seen_docs[filename] = doc_count + 1
                        deduplicated.append({
                            "content": doc_content,
                            "metadata": metadata,
                            "score": 1 - distance if distance is not None else 0.0
                        })
                
                # 🔹 Хватает top_k
                    if len(deduplicated) >= top_k:
                        break
        
        # 🔹 Логирование результатов
            filenames = [c["metadata"].get("filename") for c in deduplicated if c["metadata"].get("filename")]
            unique_files = list(set(filenames))
            logger.info(f"📚 ПОИСК: '{query[:30]}...' → чанки из: {unique_files} (всего {len(deduplicated)})")
        
            return deduplicated
            
        except Exception as e:
            logger.error(f"❌ Ошибка поиска: {type(e).__name__}: {e}", exc_info=True)
            return []
        
    async def generate_answer(
        self,
        query: str,
        user_id: str,
        chat_history: Optional[List[dict]] = None
    ) -> dict:
        
        relevant_chunks = await self.search(query, user_id, top_k=20)
        
        if not relevant_chunks:
            logger.info(f"Не найдено релевантных чанков для запроса: {query}")
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
Отвечай на русском языке, кратко и по делу."""
        
        user_prompt = f"""Контекст из документов:
{context}

Вопрос пользователя: {query}

Ответ:"""
        
        try:
            answer = await asyncio.to_thread(
                self.llm.generate,
                prompt=user_prompt,
                system=system_prompt
            )
        except Exception as e:
            logger.error(f"Ошибка генерации ответа через Ollama: {e}")
            answer = "Произошла ошибка при генерации ответа. Попробуйте позже."
        
        sources = list(set([
            chunk["metadata"].get("filename", "Unknown")
            for chunk in relevant_chunks
            if chunk["metadata"].get("filename")
        ]))
        
        logger.info(f"Ответ сгенерирован, источники: {sources}")
        
        return {
            "answer": answer,
            "sources": sources,
            "used_chunks": relevant_chunks
        }
    
    async def delete_document_from_index(self, document_id: str, user_id: str) -> bool:
        try:
            collection = self.chroma.get_or_create_collection(user_id)
            
            results = collection.get(
                where={"document_id": document_id},
                include=[]  
            )
            
            if results.get("ids") and results["ids"]:
                collection.delete(ids=results["ids"])
                logger.info(f"Удалено {len(results['ids'])} чанков документа {document_id} из индекса")
                return True
            else:
                logger.info(f"ℹДокумент {document_id} не найден в индексе пользователя {user_id}")
                return True 
                
        except Exception as e:
            logger.error(f"Ошибка удаления документа {document_id} из индекса: {e}", exc_info=True)
            return False


rag_service = RAGService(db_session=None)


def get_rag_service(db_session):
    return rag_service