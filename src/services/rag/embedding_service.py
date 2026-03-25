from src.services.rag.ollama_client import ollama_client
import logging


logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self.client = ollama_client
        logger.info("EmbeddingService инициализирован (Ollama)")
    
    def embed_text(self, text: str) -> list[float]:
        return self.client.embed_text(text)
    
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return self.client.embed_texts(texts)


embedding_service = EmbeddingService()