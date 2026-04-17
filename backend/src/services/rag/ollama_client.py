import ollama
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)


class OllamaClient:
    def __init__(self):
        self.embedding_model = settings.OLLAMA_EMBEDDING_MODEL  
        self.llm_model = settings.OLLAMA_LLM_MODEL
        
        try:
            headers = {}
            if settings.OLLAMA_TOKEN:
                headers["Authorization"] = f"Bearer {settings.OLLAMA_TOKEN}"
            
            # Инициализация клиента с заголовками
            self.client = ollama.Client(
                host=settings.OLLAMA_HOST,
                headers=headers if headers else None
            )
            
            models = self.client.list()
            model_names = [m.model for m in models.models] if hasattr(models, 'models') else []
            
            logger.info(f"Ollama подключён: {settings.OLLAMA_HOST}")
            logger.info(f"Доступные модели: {model_names}")
            
        except Exception as e:
            logger.error(f"Ошибка подключения к Ollama: {e}")
            raise
    
    def embed_text(self, text: str) -> list[float]:
        try:
            response = self.client.embeddings(
                model=self.embedding_model,
                prompt=text
            )
            return response.embedding
        except Exception as e:
            logger.error(f"Ошибка создания эмбеддинга для '{text[:50]}...': {e}")
            raise
    
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]
    
    def generate(self, prompt: str, system: str = "") -> str:
        try:
            response = self.client.generate(
                model=self.llm_model,
                prompt=prompt,
                system=system,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 2048,  
                }
            )
            return response.response
        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {e}")
            raise
    
    def chat(self, messages: list[dict], system: str = "") -> str:
        try:
            if system:
                messages = [{"role": "system", "content": system}] + messages
            
            response = self.client.chat(
                model=self.llm_model,
                messages=messages,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            )
            return response.message.content
        except Exception as e:
            logger.error(f"Ошибка чата: {e}")
            raise

ollama_client = OllamaClient()