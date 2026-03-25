import ollama
from src.core.config import settings
import logging


logger = logging.getLogger(__name__)


class OllamaClient:
    def __init__(self):
        self.host = settings.OLLAMA_HOST
        self.embedding_model = settings.OLLAMA_EMBEDDING_MODEL  
        self.llm_model = settings.OLLAMA_LLM_MODEL
        
        try:
            self.client = ollama.Client(host=self.host)
            models = self.client.list()
            logger.info(f"Ollama подключён: {self.host}")
            logger.info(f"Доступные модели: {[m['name'] for m in models['models']]}")
        except Exception as e:
            logger.error(f"Ошибка подключения к Ollama: {e}")
            raise
    
    def embed_text(self, text: str) -> list[float]:
        try:
            response = ollama.embeddings(
                model=self.embedding_model,
                prompt=text,
                host=self.host
            )
            return response["embedding"]
        except Exception as e:
            logger.error(f"Ошибка создания эмбеддинга: {e}")
            raise
    
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]
    
    def generate(self, prompt: str, system: str = "") -> str:
        try:
            response = ollama.generate(
                model=self.llm_model,
                prompt=prompt,
                system=system,
                host=self.host,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            )
            return response["response"]
        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {e}")
            raise
    
    def chat(self, messages: list[dict], system: str = "") -> str:
        try:
            if system:
                messages = [{"role": "system", "content": system}] + messages
            
            response = ollama.chat(
                model=self.llm_model,
                messages=messages,
                host=self.host,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            )
            return response["message"]["content"]
        except Exception as e:
            logger.error(f"Ошибка чата: {e}")
            raise


ollama_client = OllamaClient()