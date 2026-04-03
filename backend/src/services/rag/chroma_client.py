# backend/src/services/rag/chroma_client.py

import os
import chromadb
from chromadb.config import Settings
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)


def _create_chroma_client():
    """Внутренняя функция создания клиента"""
    is_production = settings.ENVIRONMENT == "production"
    
    if is_production:
        # Production: локальное хранилище (файлы на диске)
        logger.info("ChromaDB: используя локальное хранилище (production)")
        return chromadb.PersistentClient(
            path="/app/chroma_data",
            settings=Settings(anonymized_telemetry=False)
        )
    else:
        # Development: HTTP-клиент
        logger.info(f"ChromaDB: подключение к {settings.CHROMA_HOST}:{settings.CHROMA_PORT}")
        return chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            settings=Settings(anonymized_telemetry=False)
        )


class ChromaClient:
    def __init__(self, client=None):
        # Если клиент передан извне — используем его (для тестов)
        self.client = client or _create_chroma_client()
        
        # Создаём коллекцию если нужно
        self.collection_name = "corpknow_documents"
        try:
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"ChromaDB коллекция '{self.collection_name}' готова")
        except Exception as e:
            logger.error(f"Ошибка создания коллекции ChromaDB: {e}")
            raise
    
    def get_or_create_collection(self, name: str = None, **kwargs):
        """Получить или создать коллекцию"""
        collection_name = name or self.collection_name
        return self.client.get_or_create_collection(
            name=collection_name,
            **kwargs
        )

    def add_documents(self, ids: list[str], embeddings: list[list[float]], 
                      documents: list[str], metadatas: list[dict] = None):
        """Добавление документов в коллекцию"""
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas or [{}] * len(ids)
            )
            logger.info(f"Добавлено {len(ids)} документов в ChromaDB")
        except Exception as e:
            logger.error(f"Ошибка добавления документов: {e}")
            raise
    
    def query(self, query_embedding: list[float], n_results: int = 5):
        """Поиск похожих документов"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Ошибка поиска в ChromaDB: {e}")
            raise
    
    def delete_documents(self, ids: list[str]):
        """Удаление документов по ID"""
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Удалено {len(ids)} документов из ChromaDB")
        except Exception as e:
            logger.error(f"Ошибка удаления документов: {e}")
            raise


# ✅ ЛЕНИВАЯ ИНИЦИАЛИЗАЦИЯ — сохраняем старое имя для совместимости
_chroma_client_instance = None

def _get_chroma_client_instance():
    """Внутренняя функция для получения единственного экземпляра"""
    global _chroma_client_instance
    if _chroma_client_instance is None:
        _chroma_client_instance = ChromaClient()
    return _chroma_client_instance


# ✅ Экспортируем как модульную переменную (как было раньше)
# Но инициализация происходит только при первом обращении
class _LazyChromaClient:
    def __getattr__(self, name):
        # При первом обращении к любому атрибуту — создаём реальный клиент
        instance = _get_chroma_client_instance()
        return getattr(instance, name)


chroma_client = _LazyChromaClient()