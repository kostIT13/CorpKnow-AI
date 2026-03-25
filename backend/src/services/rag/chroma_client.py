import chromadb
from chromadb.config import Settings
from src.core.config import settings
import logging


logger = logging.getLogger(__name__)


class ChromaClient:
    def __init__(self):
        try:
            self.client = chromadb.HttpClient(
                host=settings.CHROMA_HOST,
                port=settings.CHROMA_PORT,
            )
            self.client.heartbeat()
            logger.info(f"ChromaDB подключён: {settings.CHROMA_HOST}:{settings.CHROMA_PORT}")
        except Exception as e:
            logger.error(f"Ошибка подключения к ChromaDB: {e}")
            raise
    
    def get_or_create_collection(self, user_id: str) -> chromadb.Collection:
        collection_name = f"user_{user_id}"
        collection_metadata = {
            "user_id": user_id,
            "embedding_model": settings.OLLAMA_EMBEDDING_MODEL,
            "hnsw:space": "cosine" 
        }
    
        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata=collection_metadata 
            )
            logger.debug(f"Коллекция {collection_name} готова")
            return collection
        except Exception as e:
            logger.error(f"Ошибка создания коллекции {collection_name}: {e}")
            raise
    
    def delete_collection(self, user_id: str) -> bool:
        try:
            collection_name = f"user_{user_id}"
            self.client.delete_collection(name=collection_name)
            logger.info(f"Коллекция {collection_name} удалена")
            return True
        except chromadb.exceptions.InvalidCollectionException:
            logger.warning(f"Коллекция {collection_name} не найдена")
            return False
        except Exception as e:
            logger.error(f"Ошибка удаления коллекции: {e}")
            return False
    
    def health_check(self) -> bool:
        try:
            self.client.heartbeat()
            return True
        except:
            return False


chroma_client = ChromaClient()